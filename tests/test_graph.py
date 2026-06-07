import pytest
from graphs.graph import Graph
from graphs.graph_algorithms import (
    dijkstra,
    kruskal_mst,
    prim_mst,
    shortest_path,
)


def test_bfs_dfs():
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    assert "A" in g.bfs("A")
    assert "D" in g.dfs("A")


def test_topological_sort():
    dg = Graph(directed=True)
    dg.add_edge("A", "B")
    dg.add_edge("A", "C")
    dg.add_edge("B", "D")
    order = dg.topological_sort()
    assert order.index("A") < order.index("D")


def test_dijkstra_and_path():
    g = Graph(directed=False)
    g.add_edge("S", "A", 1)
    g.add_edge("S", "B", 4)
    g.add_edge("A", "B", 2)
    g.add_edge("A", "C", 5)
    g.add_edge("B", "C", 1)

    dist, _ = dijkstra(g, "S")
    assert dist["C"] == 4
    assert shortest_path(g, "S", "C") == ["S", "A", "B", "C"]


def test_mst():
    g = Graph(directed=False)
    g.add_edge(0, 1, 1)
    g.add_edge(0, 2, 3)
    g.add_edge(1, 2, 1)

    mst_k = kruskal_mst(g)
    mst_p = prim_mst(g)
    assert len(mst_k) == 2
    assert len(mst_p) == 2
    total_k = sum(w for _, _, w in mst_k)
    assert total_k == 2  # 최소 1+1