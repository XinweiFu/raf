OP_MAP = {
    "mnm.op.abs": ["abs", "", "kElemWise"],
    "mnm.op.add": ["add", "", "kBroadcast"],
    "mnm.op.all": ["all", "relay.attrs.ReduceAttrs", "kCommReduce"],
    "mnm.op.any": ["any", "relay.attrs.ReduceAttrs", "kCommReduce"],
    "mnm.op.arange": ["arange", "relay.attrs.ArangeAttrs", "kOpaque"],
    "mnm.op.argmax": ["argmax", "relay.attrs.ReduceAttrs", "kCommReduce"],
    "mnm.op.argmin": ["argmin", "relay.attrs.ReduceAttrs", "kCommReduce"],
    "mnm.op.argsort": ["argsort", "relay.attrs.ArgsortAttrs", "kOpaque"],
    "mnm.op.argwhere": ["argwhere", "relay.attrs.ArgWhereAttrs", "kOpaque"],
    "mnm.op.atan": ["atan", "", "kElemWise"],
    "mnm.op.broadcast_to": ["broadcast_to", "", "kBroadcast"],
    "mnm.op.broadcast_to_like": ["broadcast_to_like", "", "kBroadcast"],
    "mnm.op.cast": ["cast", "relay.attrs.CastAttrs", "kElemWise"],
    "mnm.op.cast_like": ["cast_like", "", "kElemWise"],
    "mnm.op.ceil": ["ceil", "", "kElemWise"],
    "mnm.op.clip": ["clip", "relay.attrs.ClipAttrs", "kElemWise"],
    "mnm.op.collapse_sum_like": ["collapse_sum_like", "", "kCommReduce"],
    "mnm.op.concatenate": ["concatenate", "relay.attrs.ConcatenateAttrs", "kInjective"],
    "mnm.op.copy": ["copy", "", "kElemWise"],
    "mnm.op.cos": ["cos", "", "kElemWise"],
    "mnm.op.divide": ["divide", "", "kBroadcast"],
    "mnm.op.equal": ["equal", "", "kBroadcast"],
    "mnm.op.erf": ["erf", "", "kElemWise"],
    "mnm.op.exp": ["exp", "", "kElemWise"],
    "mnm.op.expand_dims": ["expand_dims", "relay.attrs.ExpandDimsAttrs", "kBroadcast"],
    "mnm.op.floor": ["floor", "", "kElemWise"],
    "mnm.op.floor_divide": ["floor_divide", "", "kBroadcast"],
    "mnm.op.floor_mod": ["floor_mod", "", "kBroadcast"],
    "mnm.op.full": ["full", "relay.attrs.InitOpAttrs", "kElemWise"],
    "mnm.op.full_like": ["full_like", "", "kElemWise"],
    "mnm.op.gather_nd": ["gather_nd", "", "kInjective"],
    "mnm.op.greater": ["greater", "", "kBroadcast"],
    "mnm.op.greater_equal": ["greater_equal", "", "kBroadcast"],
    "mnm.op.image.resize": ["image.resize", "relay.attrs.ResizeAttrs", "kInjective"],
    "mnm.op.layout_transform": ["layout_transform", "relay.attrs.LayoutTransformAttrs", "kInjective"],
    "mnm.op.left_shift": ["left_shift", "", "kBroadcast"],
    "mnm.op.less": ["less", "", "kBroadcast"],
    "mnm.op.less_equal": ["less_equal", "", "kBroadcast"],
    "mnm.op.log": ["log", "", "kElemWise"],
    "mnm.op.logical_and": ["logical_and", "", "kBroadcast"],
    "mnm.op.logical_not": ["logical_not", "", "kElemWise"],
    "mnm.op.logical_or": ["logical_or", "", "kBroadcast"],
    "mnm.op.max": ["max", "relay.attrs.ReduceAttrs", "kCommReduce"],
    "mnm.op.maximum": ["maximum", "", "kBroadcast"],
    "mnm.op.mean": ["mean", "relay.attrs.ReduceAttrs", "kCommReduce"],
    "mnm.op.min": ["min", "relay.attrs.ReduceAttrs", "kCommReduce"],
    "mnm.op.minimum": ["minimum", "", "kBroadcast"],
    "mnm.op.mod": ["mod", "", "kBroadcast"],
    "mnm.op.multiply": ["multiply", "", "kBroadcast"],
    "mnm.op.negative": ["negative", "", "kElemWise"],
    "mnm.op.bias_add": ["nn.bias_add", "relay.attrs.BiasAddAttrs", "kBroadcast"],
    "mnm.op.not_equal": ["not_equal", "", "kBroadcast"],
    "mnm.op.one_hot": ["one_hot", "relay.attrs.OneHotAttrs", "kOutEWiseFusable"],
    "mnm.op.ones": ["ones", "relay.attrs.InitOpAttrs", "kElemWise"],
    "mnm.op.ones_like": ["ones_like", "", "kElemWise"],
    "mnm.op.power": ["power", "", "kBroadcast"],
    "mnm.op.prod": ["prod", "relay.attrs.ReduceAttrs", "kCommReduce"],
    "mnm.op.reinterpret": ["reinterpret", "relay.attrs.CastAttrs", "kElemWise"],
    "mnm.op.repeat": ["repeat", "relay.attrs.RepeatAttrs", "kBroadcast"],
    "mnm.op.reverse": ["reverse", "relay.attrs.ReverseAttrs", "kInjective"],
    "mnm.op.right_shift": ["right_shift", "", "kBroadcast"],
    "mnm.op.round": ["round", "", "kElemWise"],
    "mnm.op.rsqrt": ["rsqrt", "", "kElemWise"],
    "mnm.op.sequence_mask": ["sequence_mask", "relay.attrs.SequenceMaskAttrs", "kInjective"],
    "mnm.op.sigmoid": ["sigmoid", "", "kElemWise"],
    "mnm.op.sign": ["sign", "", "kElemWise"],
    "mnm.op.sin": ["sin", "", "kElemWise"],
    "mnm.op.slice_like": ["slice_like", "relay.attrs.SliceLikeAttrs", "kInjective"],
    "mnm.op.split": ["split", "relay.attrs.SplitAttrs", "kInjective"],
    "mnm.op.sqrt": ["sqrt", "", "kElemWise"],
    "mnm.op.squeeze": ["squeeze", "relay.attrs.SqueezeAttrs", "kInjective"],
    "mnm.op.stack": ["stack", "relay.attrs.StackAttrs", "kInjective"],
    "mnm.op.strided_slice": ["strided_slice", "relay.attrs.StridedSliceAttrs", "kInjective"],
    "mnm.op.subtract": ["subtract", "", "kBroadcast"],
    "mnm.op.take": ["take", "relay.attrs.TakeAttrs", "kInjective"],
    "mnm.op.tanh": ["tanh", "", "kElemWise"],
    "mnm.op.tile": ["tile", "relay.attrs.TileAttrs", "kBroadcast"],
    "mnm.op.topk": ["topk", "relay.attrs.TopkAttrs", "kOpaque"],
    "mnm.op.transpose": ["transpose", "relay.attrs.TransposeAttrs", "kInjective"],
    "mnm.op.trunc": ["trunc", "", "kElemWise"],
    "mnm.op.variance": ["variance", "relay.attrs.ReduceAttrs", "kCommReduce"],
    "mnm.op.where": ["where", "", "kBroadcast"],
    "mnm.op.zeros": ["zeros", "relay.attrs.InitOpAttrs", "kElemWise"],
    "mnm.op.zeros_like": ["zeros_like", "", "kElemWise"],
}