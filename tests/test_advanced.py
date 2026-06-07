from advanced.union_find import UnionFind
from advanced.segment_tree import SegmentTree, SegmentTreeMin


def test_union_find():
    uf = UnionFind(list(range(10)))
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)
    assert uf.connected(0, 2)
    assert not uf.connected(0, 3)
    assert uf.count_components() == 7  # 10 - 3 unions = 7 components at this point


def test_segment_tree_sum():
    st = SegmentTree([1, 2, 3, 4, 5])
    assert st.query(0, 4) == 15
    assert st.query(1, 3) == 9
    st.update(2, 10)
    assert st.query(0, 2) == 13


def test_segment_tree_min():
    stm = SegmentTreeMin([5, 2, 8, 1, 9])
    assert stm.query(0, 4) == 1
    assert stm.query(1, 3) == 1
    stm.update(3, 0)
    assert stm.query(0, 2) == 2