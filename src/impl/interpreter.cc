#include <mnm/executor.h>
#include <mnm/ir.h>
#include <mnm/memory_pool.h>
#include <mnm/op.h>
#include <mnm/pass.h>
#include <mnm/registry.h>
#include <mnm/tensor.h>
#include <mnm/value.h>
#include "../common/arg_utils.h"
#include "../common/shape_utils.h"
#include "../requests.h"

namespace mnm {
namespace interpreter {

using namespace mnm::ir;
using namespace mnm::value;
using common::arg_utils::AsVector;
using common::shape_utils::BytesCompactTensor;
using executor::Executor;
using memory_pool::Memory;
using op::CallValues;
using op::RunDeclare;
using op::OpDispatch;
using op::OpEnv;
using op::MakeListArgs;
using op::GetListArgs;
using registry::GetPackedFunc;
using registry::PackedFunc;
using registry::TypedPackedFunc;
using requests::Requests;
using stream_pool::Stream;
using tensor::Tensor;

class Stack {
  using Frame = Map<Var, Value>;

 public:
  std::vector<Frame> frames;

  Stack() : frames() {
    frames.push_back(Frame({}));
  }

  void Extend(const Var& var, const Value& value) {
    frames.back().Set(var, value);
  }

  Value Lookup(const Var& local) {
    for (auto frame = frames.rbegin(); frame != frames.rend(); frame++) {
      auto elem = frame->find(local);
      if (elem != frame->end()) {
        return (*elem).second;
      }
    }
    LOG(FATAL) << "could not find variable binding for " << local->name_hint();
    return Value();
  }

  class LocalFrame {
   public:
    Stack& st;
    explicit LocalFrame(Stack& st, const Frame& fr) : st(st) {
      st.frames.push_back(fr);
    }
    ~LocalFrame() {
      st.frames.pop_back();
    }
  };
};

class Interpreter final : public ExprFunctor<Value(const Expr& n)>, public Executor {
 public:
  Module mod;
  Stack stack;
  std::unordered_map<const ExprNode*, const BoundExprNode*> bindings;

 public:
  Interpreter(Module mod) : mod(mod) {
  }

  ~Interpreter() = default;

  Value Eval(const Expr& expr) {
    const ExprNode* node = expr.as_derived<ExprNode>();
    CHECK(node != nullptr);
    if (bindings.count(node)) {
      return bindings[node]->value;
    }
    return ExprFunctor<Value(const Expr& n)>::VisitExpr(expr);
  }

  Value VisitExpr(const Expr& expr) override {
    return Eval(expr);
  }

  Value VisitExpr_(const VarNode* node) override {
    return stack.Lookup(GetRef<Var>(node));
  }

  Value VisitExpr_(const GlobalVarNode* node) override {
    return Eval(mod->Lookup(GetRef<GlobalVar>(node)));
  }

  Value VisitExpr_(const OpNode* node) override {
    // Q: Why not do eta-expansion?
    // A: Sometimes the frontend may be interested in knowning the op.
    return OpValue::make(GetRef<Op>(node));
  }

  Value VisitExpr_(const FunctionNode* node) override {
    const Function& func = GetRef<Function>(node);
    Map<Var, Value> captured_mod;
    Array<Var> free_vars = pass::FreeVars(func);
    for (const auto& var : free_vars) {
      captured_mod.Set(var, Eval(var));
    }
    return ClosureValue::make(captured_mod, func);
  }

  Value VisitExpr_(const CallNode* node) override {
    static auto fschema = Op::GetAttr<op::FMNMSchema>("FMNMSchema");
    const Call& call = GetRef<Call>(node);
    Array<Value> args;
    for (auto arg : call->args) {
      args.push_back(Eval(arg));
    }
    CallValues call_values = CallValues::make();
    call_values->callee = Eval(call->op);
    if (call_values->callee->is_type<ClosureValueNode>()) {
      call_values->args = MakeListArgs(args);
      return InvokeClosure(call_values);
    } else if (const auto* op = call_values->callee.as<OpValueNode>()) {
      call_values->args = fschema[op->op](args);
      return InvokePrimitive(call_values);
    }
    LOG(FATAL) << "ValueError: type " << call_values->callee->type_key() << " is not callable";
    throw;
  }

  Value VisitExpr_(const RelayConstantNode* _node) override {
    const ConstantNode* node = static_cast<const ConstantNode*>(_node);
    return Downcast<Value>(node->value);
  }

  Value VisitExpr_(const LetNode* node) override {
    stack.Extend(node->var, Eval(node->value));
    return Eval(node->body);
  }

  Value VisitExpr_(const IfNode* node) override {
    bool result = Downcast<BoolValue>(Eval(node->cond))->data;
    return result ? Eval(node->true_branch) : Eval(node->false_branch);
  }

  Value VisitExpr_(const TupleNode* node) override {
    std::vector<Value> values;
    for (const Expr& field : node->fields) {
      values.push_back(Eval(field));
    }
    return TupleValue::make(values);
  }

  Value VisitExpr_(const TupleGetItemNode* node) override {
    TupleValue tuple = Downcast<TupleValue>(Eval(node->tuple));
    int index = node->index;
    int size = static_cast<int>(tuple->fields.size());
    CHECK(0 <= index && index < size) << "IndexError: tuple index out of range";
    Value sub_value = tuple->fields[index];
    if (sub_value->op_env == nullptr) {
      sub_value->op_env = tuple->op_env;
    }
    return sub_value;
  }

  Value VisitExpr_(const RefCreateNode* node) override {
    return RefValue::make(Eval(node->value));
  }

  Value VisitExpr_(const RefReadNode* node) override {
    return Downcast<RefValue>(Eval(node->ref))->value;
  }

  Value VisitExpr_(const RefWriteNode* node) override {
    Downcast<RefValue>(Eval(node->ref))->value = Eval(node->value);
    return TupleValue::make({});
  }

 public:
  Value InvokePrimitive(const CallValues& call) {
    const Op& op = Downcast<OpValue>(call->callee)->op;
    RunDeclare(call);
    if (!call->callee.defined()) {
      return call->out;
    }
    std::unique_ptr<OpEnv> op_env = OpDispatch::Dispatch(call);
    if (op_env != nullptr) {
      InvokePrimitiveOpEnv(std::move(op_env), call);
    } else {
      LOG(FATAL) << "ValueError: Cannot dispatch " << op->name << "@" << call->ctx.c_str();
      throw;
    }
    return call->out;
  }

  void InvokePrimitiveOpEnv(std::unique_ptr<OpEnv> op_env, const CallValues& call) {
    std::shared_ptr<Requests> req = op_env->GetRequests();
    {
      for (int i = 0, n = req->memory.size(); i < n; ++i) {
        RequestMemory(req.get(), i);
      }
      for (int i = 0, n = req->workspace.size(); i < n; ++i) {
        RequestWorkspace(req.get(), i);
      }
      for (int i = 0, n = req->stream.size(); i < n; ++i) {
        RequestStream(req.get(), i);
      }
    }
    op_env->Execute(call);
    {
      for (int i = 0, n = req->stream.size(); i < n; ++i) {
        req->stream[i].stream->Wait();
      }
      req->workspace.clear();
      req->workspace.shrink_to_fit();
      req->stream.clear();
      req->stream.shrink_to_fit();
    }
    call->out->op_env = std::move(op_env);
  }

 public:
  Value InvokeClosure(const CallValues& call) {
    const auto* node = call->callee.as<ClosureValueNode>();
    const Function& func = node->func;
    const Array<Value>& call_args = GetListArgs(call->args);
    Map<Var, Value> locals;
    CHECK_EQ(func->params.size(), call_args.size());
    int n_args = call_args.size();
    for (int i = 0; i < n_args; ++i) {
      locals.Set(func->params[i], call_args[i]);
    }
    for (auto it = node->env.begin(); it != node->env.end(); ++it) {
      locals.Set((*it).first, (*it).second);
    }
    {
      Stack::LocalFrame lf(stack, std::move(locals));
      return Eval(func->body);
    }
  }

 public:
  void OnBind(const op::OpEnv* op_env) override {
  }

  void OnDestruct(const op::OpEnv* op_env) override {
  }

  void OnBind(const BoundExprNode* bound_expr) override {
    const ExprNode* expr = bound_expr->expr.as_derived<ExprNode>();
    CHECK(expr != nullptr);
    CHECK_EQ(bindings.count(expr), 0);
    bindings[expr] = bound_expr;
  }

  void OnDestruct(const BoundExprNode* bound_expr) override {
    const ExprNode* expr = bound_expr->expr.as_derived<ExprNode>();
    CHECK(expr != nullptr);
    CHECK_NE(bindings.count(expr), 0);
    bindings.erase(expr);
  }

  void RequestMemory(Requests* req, int index) override {
    Requests::MemoryRequest& entry = req->memory[index];
    CHECK(entry.memory == nullptr);
    std::shared_ptr<Memory> memory = Memory::Alloc(entry.ctx, entry.nbytes);
    *entry.dest = memory->data;
    entry.memory = memory;
  }

  void RequestWorkspace(Requests* req, int index) override {
    Requests::WorkspaceRequest& entry = req->workspace[index];
    CHECK(entry.memory == nullptr);
    std::shared_ptr<Memory> memory = Memory::Alloc(entry.ctx, entry.nbytes);
    *entry.dest = memory->data;
    entry.memory = memory;
  }

  void RequestStream(Requests* req, int index) override {
    Requests::StreamRequest& entry = req->stream[index];
    std::shared_ptr<Stream> stream = Stream::Get(entry.ctx, entry.tag_idx, entry.stream_idx);
    *entry.dest = stream->data();
    entry.stream = stream;
  }
};

static NodeRef DeTuple(const Expr& expr, const Value& value, Executor* executor) {
  // make nested lists of BoundExpr
  if (value->derived_from<ScalarValueNode>()) {
    return value;
  }
  if (value->is_type<TensorValueNode>()) {
    BoundExpr ret = BoundExpr::make(expr, value);
    ret->BindExecutor(executor);
    return std::move(ret);
  }
  if (const auto* tuple = value.as<TupleValueNode>()) {
    Array<NodeRef> result;
    int n = static_cast<int>(tuple->fields.size());
    for (int i = 0; i < n; ++i) {
      Expr sub_expr = ir::TupleGetItemNode::make(expr, i);
      Value sub_value = tuple->fields[i];
      if (sub_value->op_env == nullptr) {
        sub_value->op_env = tuple->op_env;
      }
      result.push_back(DeTuple(expr, value, executor));
    }
    return std::move(result);
  }
  LOG(FATAL) << "ValueError: cannot de-tuple " << value->type_key();
  throw;
}

TypedPackedFunc<NodeRef(Expr)> CreateInterpreter(Module module) {
  auto intrp = std::make_shared<Interpreter>(module);
  auto packed = [intrp](Expr expr) {
    Value value = intrp->Eval(expr);
    return DeTuple(expr, value, intrp.get());
  };
  return TypedPackedFunc<NodeRef(Expr)>(packed);
}

MNM_REGISTER_GLOBAL("mnm.executor.CreateInterpreter").set_body_typed(CreateInterpreter);

}  // namespace interpreter
}  // namespace mnm