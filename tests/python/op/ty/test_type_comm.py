"""Test collective communication operators in a cluster with 2 GPUs.
As pytest do not support mpirun, thus we skip this test in pytest progress.
To test collective_communication, you should run:
`mpirun -np 2 python3 tests/python/op/ty/test_type_comm.py`
(in ci/task_python_unittest.sh)
"""
import pytest
import numpy as np
import mnm
from mnm import distributed as dist
from mnm.testing import check_type, run_infer_type
from tvm.relay import TensorType, FuncType, TupleType


def get_node_info():
    dctx = dist.get_context()
    root_rank = dctx.root_rank
    rank = dctx.rank
    size = dctx.size
    local_rank = dctx.local_rank
    local_size = dctx.local_size

    if rank == 0:
        node_info = f"root_rank={root_rank},rank={rank}, \
        size={size},local_rank={local_rank}, local_size={local_size} "
        print(node_info)
    return rank, local_rank


# pylint: disable=no-member, no-self-use, protected-access, too-many-locals
@pytest.mark.skip()
def test_allreduce_with_tensor():
    print("Testing allreduce with a single tensor as input.")

    class TestModel(mnm.Model):
        def build(self):
            pass
        @mnm.model.trace
        def forward(self, x):  # pylint: disable=no-self-use,invalid-name
            x = mnm.allreduce(x)
            return x

    shape = (4, 4)
    dtype = "float32"
    model = TestModel()
    rank, local_rank = get_node_info()
    ctx = f"cuda({local_rank})"
    x = np.ones(shape=shape, dtype=dtype) * (rank+1)
    x = mnm.array(x, ctx=ctx)
    m_func = model.get_relay_func(x)
    m_func = run_infer_type(m_func)
    t_a = TensorType(shape, dtype=dtype)
    t_b = TensorType(shape, dtype=dtype)
    desire_type = FuncType([t_a], TupleType([t_b]))
    check_type(m_func, desire_type)


# pylint: disable=no-member, no-self-use, protected-access, too-many-locals
@pytest.mark.skip()
def test_allreduce_with_tensor_list():
    print("Testing allreduce with a list of tensors as input.")

    class TestModel(mnm.Model):
        def build(self):
            pass
        @mnm.model.trace
        def forward(self, x1, x2):  # pylint: disable=no-self-use
            x = mnm.allreduce([x1, x2])  # pylint: disable=invalid-name
            return x

    shape1 = (4, 4)
    shape2 = (3, 4, 5)
    dtype = "float32"
    model = TestModel()
    rank, local_rank = get_node_info()
    ctx = f"cuda({local_rank})"
    x1 = np.ones(shape=shape1, dtype=dtype) * (rank+1)
    x2 = np.ones(shape=shape2, dtype=dtype) * (-rank-1)
    x1 = mnm.array(x1, ctx=ctx)
    x2 = mnm.array(x2, ctx=ctx)
    # infertype test for list of input
    m_func = model.get_relay_func(x1, x2)
    m_func = run_infer_type(m_func)
    t_x1 = TensorType(shape1, dtype=dtype)
    t_x2 = TensorType(shape2, dtype=dtype)
    desire_type = FuncType([t_x1, t_x2], TupleType([t_x1, t_x2]))
    check_type(m_func, desire_type)


if __name__ == "__main__":
    if mnm.build.with_distributed():
        test_allreduce_with_tensor()
        test_allreduce_with_tensor_list()
        dist.RemoveCommunicator()