from . import def_schema
from .codegen_utils import Op

OPS = [
    Op(name="arange", schema_name="arange"),
    Op(name="adv_index", schema_name="adv_index"),
    Op(name="adv_index_dx", schema_name="adv_index_dx"),
    Op(name="atan", schema_name="unary"),
    Op(name="conv2d", schema_name="conv"),
    Op(name="conv2d_transpose", schema_name="conv_trans"),
    Op(name="max_pool2d", schema_name="pool"),
    Op(name="avg_pool2d", schema_name="pool"),
    Op(name="adaptive_max_pool2d", schema_name="adaptive_pool"),
    Op(name="adaptive_avg_pool2d", schema_name="adaptive_pool"),
    Op(name="softmax", schema_name="softmax"),
    Op(name="pad", schema_name="pad"),
    Op(name="log_softmax", schema_name="softmax"),
    Op(name="batch_norm_train", schema_name="batch_norm"),
    Op(name="batch_norm_infer", schema_name="batch_norm"),
    Op(name="batch_norm_train_dxwb", schema_name="batch_norm_train_dxwb"),
    Op(name="conv2d_dx", schema_name="conv_dxw"),
    Op(name="conv2d_dw", schema_name="conv_dxw"),
    Op(name="conv2d_transpose_dx", schema_name="conv_transpose_dxw"),
    Op(name="conv2d_transpose_dw", schema_name="conv_transpose_dxw"),
    Op(name="max_pool2d_dx", schema_name="pool_dx"),
    Op(name="avg_pool2d_dx", schema_name="pool_dx"),
    Op(name="adaptive_max_pool2d_dx", schema_name="adaptive_pool_dx"),
    Op(name="adaptive_avg_pool2d_dx", schema_name="adaptive_pool_dx"),
    Op(name="softmax_dx", schema_name="softmax_dx"),
    Op(name="log_softmax_dx", schema_name="softmax_dx"),
    Op(name="batch_flatten", schema_name="unary"),
    Op(name="negative", schema_name="unary"),
    Op(name="logical_not", schema_name="unary"),
    Op(name="relu", schema_name="unary"),
    Op(name="gelu", schema_name="unary"),
    Op(name="tanh", schema_name="unary"),
    Op(name="copy", schema_name="unary"),
    Op(name="abs", schema_name="unary"),
    Op(name="all", schema_name="reduce"),
    Op(name="any", schema_name="reduce"),
    Op(name="ceil", schema_name="unary"),
    Op(name="cos", schema_name="unary"),
    Op(name="sin", schema_name="unary"),
    Op(name="sign", schema_name="unary"),
    Op(name="round", schema_name="unary"),
    Op(name="floor", schema_name="unary"),
    Op(name="log", schema_name="unary"),
    Op(name="log2", schema_name="unary"),
    Op(name="exp", schema_name="unary"),
    Op(name="sigmoid", schema_name="unary"),
    Op(name="erf", schema_name="unary"),
    Op(name="sqrt", schema_name="unary"),
    Op(name="rsqrt", schema_name="unary"),
    Op(name="relu_dx", schema_name="unary_dx"),
    Op(name="gelu_dx", schema_name="unary_dx"),
    Op(name="tanh_dx", schema_name="unary_dx"),
    Op(name="sigmoid_dx", schema_name="unary_dx"),
    Op(name="erf_dx", schema_name="unary_dx"),
    Op(name="sqrt_dx", schema_name="unary_dx"),
    Op(name="add", schema_name="binary_ufunc"),
    Op(name="subtract", schema_name="binary_ufunc"),
    Op(name="multiply", schema_name="binary"),
    Op(name="divide", schema_name="binary"),
    Op(name="floor_divide", schema_name="binary"),
    Op(name="power", schema_name="binary"),
    Op(name="mod", schema_name="binary"),
    Op(name="less", schema_name="binary"),
    Op(name="greater", schema_name="binary"),
    Op(name="less_equal", schema_name="binary"),
    Op(name="greater_equal", schema_name="binary"),
    Op(name="equal", schema_name="binary"),
    Op(name="not_equal", schema_name="binary"),
    Op(name="maximum", schema_name="binary"),
    Op(name="minimum", schema_name="binary"),
    Op(name="right_shift", schema_name="binary"),
    Op(name="trunc", schema_name="unary"),
    Op(name="mesh_grid", schema_name="mesh_grid"),
    Op(name="matmul", schema_name="binary"),
    Op(name="matmul_nt", schema_name="binary"),
    Op(name="matmul_tn", schema_name="binary"),
    Op(name="matmul_tt", schema_name="binary"),
    Op(name="batch_matmul", schema_name="binary"),
    Op(name="batch_matmul_nt", schema_name="binary"),
    Op(name="batch_matmul_tn", schema_name="binary"),
    Op(name="batch_matmul_tt", schema_name="binary"),
    Op(name="smooth_l1_loss", schema_name="loss"),
    Op(name="smooth_l1_loss_dpred", schema_name="loss"),
    Op(name="smooth_l1_loss_dtrue", schema_name="loss"),
    Op(name="nll_loss", schema_name="loss"),
    Op(name="nll_loss_dpred", schema_name="loss_dtp"),
    Op(name="nll_loss_dtrue", schema_name="loss_dtp"),
    Op(name="cross_entropy", schema_name="loss"),
    Op(name="cross_entropy_dpred", schema_name="loss"),
    Op(name="cross_entropy_dtrue", schema_name="loss"),
    Op(name="reshape", schema_name="reshape"),
    Op(name="resize2d", schema_name="resize2d"),
    Op(name="ndarray_size", schema_name="unary"),
    Op(name="transpose", schema_name="transpose"),
    Op(name="transpose_dx", schema_name="transpose_dx"),
    Op(name="collapse_sum_like", schema_name="collapse_like"),
    Op(name="sum", schema_name="sum"),
    Op(name="sum_dx", schema_name="sum_dx"),
    Op(name="argmax", schema_name="reduce"),
    Op(name="argmin", schema_name="reduce"),
    Op(name="prod", schema_name="reduce"),
    Op(name="prod_dx", schema_name="prod_dx"),
    Op(name="max", schema_name="reduce"),
    Op(name="min", schema_name="reduce"),
    Op(name="mean", schema_name="reduce"),
    Op(name="mean_dx", schema_name="mean_dx"),
    Op(name="get_reduce_axis", schema_name="binary"),
    Op(name="get_kept_dims", schema_name="binary"),
    Op(name="sgd", schema_name="sgd"),
    Op(name="shape", schema_name="unary"),
    Op(name="swap_axis", schema_name="swap_axis"),
    Op(name="take", schema_name="take"),
    Op(name="take_dx", schema_name="take_dx"),
    Op(name="embedding", schema_name="embedding"),
    Op(name="embedding_dx", schema_name="embedding_dx"),
    Op(name="dense", schema_name="binary"),
    Op(name="repeat", schema_name="repeat"),
    Op(name="repeat_dx", schema_name="repeat_dx"),
    Op(name="expand_dims", schema_name="expand_dims"),
    Op(name="threefry_generate", schema_name="threefry_generate"),
    Op(name="threefry_split", schema_name="threefry_split"),
    Op(name="strided_slice", schema_name="strided_slice"),
    Op(name="strided_slice_dx", schema_name="strided_slice_dx"),
    Op(name="sequence_mask", schema_name="sequence_mask"),
    Op(name="reverse_sequence", schema_name="reverse_sequence"),
    Op(name="reverse", schema_name="reverse"),
    Op(name="broadcast_to", schema_name="broadcast_to"),
    Op(name="broadcast_to_like", schema_name="broadcast_to_like"),
    Op(name="concatenate", schema_name="concatenate"),
    Op(name="squeeze", schema_name="squeeze"),
    Op(name="stack", schema_name="stack"),
    Op(name="split", schema_name="split"),
    Op(name="threshold", schema_name="threshold"),
    Op(name="threshold_dx", schema_name="threshold_dx"),
    Op(name="layer_norm", schema_name="layer_norm"),
    Op(name="scatter", schema_name="scatter"),
    Op(name="scatter_dx", schema_name="scatter_dx"),
    Op(name="layer_norm_dx", schema_name="layer_norm_dx"),
    Op(name="concatenate_dx", schema_name="concatenate"),
    Op(name="clip", schema_name="clip"),
    Op(name="clip_dx", schema_name="clip_dx"),
    Op(name="get_valid_counts", schema_name="get_valid_counts"),
    Op(name="bias_add", schema_name="bias_add"),
    Op(name="_contrib_dropout", schema_name="dropout"),
    Op(name="_contrib_dropout_dx", schema_name="dropout_dx"),
    Op(name="non_max_suppression", schema_name="non_max_suppression"),
    Op(name="stream_sync", schema_name="stream"),
    Op(name="cast", schema_name="cast"),
    Op(name="cast_like", schema_name="cast_like"),
    Op(name="gather", schema_name="gather"),
    Op(name="gather_dx", schema_name="gather_dx"),
    Op(name="gather_nd", schema_name="gather_nd"),
    Op(name="gather_nd_dx", schema_name="gather_nd_dx"),
    Op(name="argsort", schema_name="argsort"),
    Op(name="sort", schema_name="sort"),
    Op(name="compiler_begin", schema_name="compiler"),
    Op(name="compiler_end", schema_name="compiler"),
    Op(name="full", schema_name="full"),
    Op(name="full_like", schema_name="full_like"),
    Op(name="where", schema_name="where"),
    Op(name="logical_and", schema_name="binary"),
    Op(name="device_copy", schema_name="device_copy"),
    Op(name="topk", schema_name="topk"),
    Op(name="zeros", schema_name="init_op"),
    Op(name="zeros_like", schema_name="unary"),
    Op(name="ones", schema_name="init_op"),
    Op(name="ones_like", schema_name="unary"),
    Op(name="one_hot", schema_name="one_hot"),
    Op(name="left_shift", schema_name="binary"),
    Op(name="argwhere", schema_name="argwhere"),
    Op(name="upper_bound.argwhere", schema_name="argwhere"),
    Op(name="roi_align", schema_name="roi_align"),
    Op(name="roi_align_dx", schema_name="roi_align_dx"),
    Op(name="stream_start", schema_name="stream"),
    Op(name="stream_end", schema_name="stream"),
    Op(name="stream_wait", schema_name="stream"),
    # Communication ops
    # Using underscore before the op name is because these ops won't be directly used in the
    # frontend and the wrapper ops are defined in python/mnm/distributed/op.py
    Op(name="_allreduce", schema_name="allreduce"),
    Op(name="_allgather", schema_name="allgather"),
    Op(name="_reduce_scatter", schema_name="reduce_scatter"),
    Op(name="_send", schema_name="send"),
    Op(name="_recv", schema_name="recv"),
    # VM ops
    Op(name="vm.alloc_storage", schema_name="alloc_storage"),
    Op(name="vm.alloc_tensor", schema_name="alloc_tensor"),
    Op(name="vm.free", schema_name="free"),
    Op(name="vm.invoke_op", schema_name="invoke_op"),
    Op(name="vm.infer_type", schema_name="infer_type"),
    Op(name="vm.set_shape", schema_name="set_shape"),
]

def by_name():
    result = dict()
    schemas = def_schema.by_name()

    for op in OPS:
        op.schema = schemas[op.schema_name]
        result[op.name] = op

    return result
