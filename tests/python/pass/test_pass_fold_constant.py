import pytest
import mnm
from mnm.testing import get_device_list, randn, check
import tvm

@pytest.mark.parametrize("device", get_device_list())
@pytest.mark.parametrize("shape", [
    [3, 3],
    [4, 4]
])
def test_fold_const_model(device, shape):
    const, _ = randn(shape, device=device)
    class ModelWithConst(mnm.Model):
        # pylint: disable=attribute-defined-outside-init
        def build(self):
            self.c = const

        @mnm.model.trace
        def forward(self, x):  # pylint: disable=no-self-use
            y = mnm.add(self.c, self.c)
            return mnm.add(x, y)

    model = ModelWithConst()
    m_x, _ = randn(shape, device=device, requires_grad=True)
    m_y = model(m_x)
    m_dy, n_dy = randn(shape, device=device)
    m_y.backward(m_dy)
    m_dx = m_x.grad
    n_dx = 1 * n_dy
    check(m_dx, n_dx)
    check(m_y, mnm.add(mnm.add(const, const), m_x).asnumpy())


@pytest.mark.parametrize("device", get_device_list()[1:])
@pytest.mark.parametrize("shape", [
    [3, 3],
    [4, 4]
])
def test_fold_const_ir(device, shape):
    # pylint: disable=protected-access
    const, _ = randn(shape, device=device)
    class ModelWithConst(mnm.Model):
        # pylint: disable=attribute-defined-outside-init
        def build(self):
            self.c = const

        @mnm.model.trace
        def forward(self, x):  # pylint: disable=no-self-use
            y = mnm.matmul(self.c, self.c)
            z = mnm.matmul(x, y)
            return mnm.matmul(x, z)

    def expected():
        x = tvm.relay.var('x', tvm.relay.TensorType(shape))
        c = tvm.relay.var('c', tvm.relay.TensorType(shape))
        # we are only interested in the structure
        t_value = mnm._core.value.TensorValue.from_numpy(const.asnumpy())
        const_var = mnm._ffi.ir._make.Constant(t_value)
        matmul_op = mnm._ffi.op.GetOp('mnm.op.matmul')
        closure2 = tvm.relay.Call(matmul_op, [x, const_var])
        var_a2 = tvm.relay.var('a2')
        var_a3 = tvm.relay.var('a3')
        closure3 = tvm.relay.Call(matmul_op, [x, var_a2])
        let3 = tvm.relay.Let(var_a3, closure3, var_a3)
        let2 = tvm.relay.Let(var_a2, closure2, let3)
        return tvm.relay.Function([x, c], let2)

    model_before = ModelWithConst()
    model_before.infer_mode()
    m_x, _ = randn(shape, device=device, requires_grad=True)

    func_before = model_before._internal(m_x).mod['main']

    # bind parameters
    args = [m_x._ndarray__handle, model_before.c._ndarray__handle]
    func_bound = mnm._ffi.pass_.BindParam(func_before, args)

    # fold constant
    func_folded = mnm._ffi.pass_.FoldConstant(func_bound, mnm._ffi.ir.module.Global())

    func_expected = expected()

    assert tvm.ir.structural_equal(func_folded, func_expected)


if __name__ == "__main__":
    pytest.main([__file__])
