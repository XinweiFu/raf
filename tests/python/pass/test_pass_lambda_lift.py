import pytest
import mnm
from mnm.testing import randn, get_device_list

@pytest.mark.parametrize("device", get_device_list())
@pytest.mark.parametrize("shape", [
    [3, 3],
    [4, 4]
])
def test_basic(device, shape):
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
    m_x, _ = randn(shape, device=device, requires_grad=True)
    m_y, _ = randn(shape, device=device, requires_grad=True)
    record = model._internal(m_x, m_y)
    mod = record.mod

    # Run AutoDiff to get nested functions
    # The backward function will be lifted
    mod = mnm._ffi.pass_.AutoDiff(mod, record.requires_grads)

    # Call Lambda lift pass on the Meta module
    lifted_mod = mnm._ffi.pass_.LambdaLift(mod)

    assert len(lifted_mod.functions) == 2


if __name__ == "__main__":
    pytest.main([__file__])
