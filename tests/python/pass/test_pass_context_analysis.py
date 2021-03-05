import pytest
import mnm
from mnm.testing import randn
from mnm._lib import relay, tvm
from mnm._core.module import Module
from mnm._ffi.pass_ import ContextAnalysis, FromRelay, InferType
# pylint: disable=invalid-name, no-self-use, redefined-builtin, too-many-locals, unused-variable


@pytest.mark.parametrize("ctx", mnm.testing.get_device_list())
@pytest.mark.parametrize("shape", [
    [3, 3],
    [4, 4]
])
def test_basic(ctx, shape):
    # pylint: disable=protected-access
    # Create a symbolic model and run it
    class Add(mnm.Model):
        # pylint: disable=attribute-defined-outside-init
        def build(self):
            pass

        @mnm.model.trace
        def forward(self, x, y):  # pylint: disable=no-self-use
            return mnm.add(x, y)

    # Get a Relay func
    model = Add()
    m_x, _ = randn(shape, device=ctx)
    m_y, _ = randn(shape, device=ctx)
    _ = model(m_x, m_y)
    func = model._internal().mod['main']

    # Create a Meta module and set the func as main
    mod = Module.from_expr(func)
    # Propagate types.
    mod = InferType(mod)

    dev = tvm.gpu() if ctx == "cuda" else tvm.cpu()
    # Performance context analysis
    ca = ContextAnalysis(mod, dev)

    # No device info is propagated. Everything is on the default device.
    dev_type = dev.device_type
    for _, dev in ca.items():
        assert dev[0].value == dev_type


def test_device_copy():
    if not mnm.build.with_cuda():
        return

    x = relay.var("x", shape=(2, 3))
    y = relay.var("y", shape=(2, 3))
    x1 = relay.op.device_copy(x, tvm.cpu(), tvm.gpu())
    y1 = relay.op.device_copy(y, tvm.cpu(), tvm.gpu())
    out = x1 + y1
    func = relay.Function([x, y], out)
    mod = tvm.IRModule.from_expr(func)
    # Create a Meta module and set the func as main
    mod = FromRelay(mod)
    mod = InferType(mod)
    ca = ContextAnalysis(mod, tvm.cpu())

    cpu_dev = tvm.cpu().device_type
    gpu_dev = tvm.gpu().device_type
    for expr, dev in ca.items():
        if isinstance(expr, relay.Call):
            assert dev[0].value == gpu_dev
        elif isinstance(expr, relay.Var):
            if expr.name_hint == "x" or expr.name_hint == "y":
                assert dev[0].value == cpu_dev
            else:
                assert dev[0].value == gpu_dev
        elif isinstance(expr, relay.Constant):
            assert dev[0].value == gpu_dev


@pytest.mark.skip(reason="Enable the test when vm dialects have type inference.")
@pytest.mark.parametrize("shape", [
    [3, 3],
])
def test_memory_alloc(shape):
    if not mnm.build.with_cuda():
        return

    ctx = "cuda"
    # pylint: disable=protected-access

    class Model(mnm.Model):
        # pylint: disable=attribute-defined-outside-init
        def build(self):
            pass

        @mnm.model.trace
        def forward(self, x):  # pylint: disable=no-self-use
            y = mnm.add(x, x)
            z = mnm.add(x, y)
            return z

    model_before = Model()
    model_before.infer_mode()
    m_x, _ = randn(shape, device=ctx)
    func = model_before._internal(m_x).mod['main']
    mod = Module.from_expr(func)
    mod = InferType(mod)
    with tvm.target.Target(ctx):
        mod = mnm._ffi.pass_.ManifestAlloc(mod)
    mod = InferType(mod)
    ca = ContextAnalysis(mod, tvm.cpu())
    # TODO(zhiics) Check device info of different nodes.


if __name__ == "__main__":
    pytest.main([__file__])
