"""
그래프 알고리즘 모음 (대학 과정 핵심)

포함:
- BFS / DFS (기본)
- Dijkstra (최단 경로, 음수 간선 없음)
- Bellman-Ford (음수 간선 허용, 음수 사이클 검출)
- Kruskal (MST) + Union-Find 사용
- Prim (MST)
- Topological Sort (이미 graph.py에 있음)

모두 O((V+E) log V) 또는 그에 준하는 수준
"""

from typing import Any, Dict, List, Optional, Tuple
from collections import deque
import heapq
from .graph import Graph


# ==================== 최단 경로 ====================

def dijkstra(g: Graph, start: Any) -> Tuple[Dict[Any, float], Dict[Any, Any]]:
    """
    다익스트라 최단 경로 알고리즘
    반환: (distances, previous)
    """
    if start not in g.vertices():
        raise ValueError("Start vertex not in graph")

    dist: Dict[Any, float] = {v: float("inf") for v in g.vertices()}
    prev: Dict[Any, Any] = {v: None for v in g.vertices()}
    dist[start] = 0

    pq: List[Tuple[float, Any]] = [(0, start)]  # (distance, vertex)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g.neighbors(u):
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v))

    return dist, prev


def bellman_ford(g: Graph, start: Any) -> Tuple[Dict[Any, float], Dict[Any, Any], bool]:
    """
    Bellman-Ford 알고리즘 (음수 가중치 허용)
    반환: (dist, prev, has_negative_cycle)
    """
    dist: Dict[Any, float] = {v: float("inf") for v in g.vertices()}
    prev: Dict[Any, Any] = {v: None for v in g.vertices()}
    dist[start] = 0

    # V-1 번 relaxation
    for _ in range(len(g.vertices()) - 1):
        for u, v, w in g.edges():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

    # 음수 사이클 검출
    has_neg = False
    for u, v, w in g.edges():
        if dist[u] + w < dist[v]:
            has_neg = True
            break

    return dist, prev, has_neg


def reconstruct_path(prev: Dict[Any, Any], target: Any) -> List[Any]:
    """previous 딕셔너리로 경로 복원"""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev[current]
    return path[::-1]


# ==================== 최소 신장 트리 (MST) ====================

class _DSU:
    """Kruskal용 간단 Union-Find (advanced/union_find.py와 동일 로직)"""
    def __init__(self, vertices: List[Any]):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, x: Any) -> Any:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: Any, y: Any) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True


def kruskal_mst(g: Graph) -> List[Tuple[Any, Any, float]]:
    """
    Kruskal 알고리즘으로 MST 간선 반환
    무방향 가중 그래프에서만 동작
    """
    if g.directed:
        raise ValueError("Kruskal only works on undirected graphs")

    edges = sorted(g.edges(), key=lambda e: e[2])  # 가중치 오름차순
    dsu = _DSU(g.vertices())
    mst_edges = []

    for u, v, w in edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            if len(mst_edges) == len(g.vertices()) - 1:
                break
    return mst_edges


def prim_mst(g: Graph, start: Optional[Any] = None) -> List[Tuple[Any, Any, float]]:
    """
    Prim 알고리즘 (우선순위 큐 사용)
    """
    if g.directed:
        raise ValueError("Prim only works on undirected graphs")
    if not g.vertices():
        return []

    if start is None:
        start = g.vertices()[0]

    mst_edges: List[Tuple[Any, Any, float]] = []
    visited: set = set([start])
    # (weight, u, v) 형태로 저장 — u는 이미 visited, v가 새로 추가될 정점
    pq: List[Tuple[float, Any, Any]] = []

    for v, w in g.neighbors(start):
        heapq.heappush(pq, (w, start, v))

    while pq and len(visited) < len(g.vertices()):
        w, u, v = heapq.heappop(pq)
        if v in visited:
            continue
        visited.add(v)
        mst_edges.append((u, v, w))

        for to, weight in g.neighbors(v):
            if to not in visited:
                heapq.heappush(pq, (weight, v, to))

    return mst_edges


# ==================== 유틸 ====================

def shortest_path(g: Graph, start: Any, target: Any) -> Optional[List[Any]]:
    """Dijkstra를 이용한 최단 경로 복원 (음수 없다고 가정)"""
    dist, prev = dijkstra(g, start)
    if dist[target] == float("inf"):
        return None
    return reconstruct_path(prev, target)


if __name__ == "__main__":
    # Dijkstra 데모
    g = Graph(directed=False)
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 1)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 8)
    g.add_edge("C", "E", 10)
    g.add_edge("D", "E", 2)

    dist, prev = dijkstra(g, "A")
    print("Dijkstra distances from A:", dist)
    print("Shortest path A->E:", shortest_path(g, "A", "E"))

    # MST 데모
    ug = Graph(directed=False)
    ug.add_edge(0, 1, 4)
    ug.add_edge(0, 7, 8)
    ug.add_edge(1, 2, 8)
    ug.add_edge(1, 7, 11)
    ug.add_edge(2, 3, 7)
    ug.add_edge(2, 5, 4)
    ug.add_edge(2, 8, 2)
    ug.add_edge(3, 4, 9)
    ug.add_edge(3, 5, 14)
    ug.add_edge(4, 5, 10)
    ug.add_edge(5, 6, 2)
    ug.add_edge(6, 7, 1)
    ug.add_edge(6, 8, 6)
    ug.add_edge(7, 8, 7)

    print("\nKruskal MST edges:", kruskal_mst(ug))
    print("Prim MST edges:", prim_mst(ug))