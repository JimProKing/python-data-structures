"""
Graph (그래프) — 인접 리스트(Adjacency List) 중심 구현

지원:
- 무방향 / 방향 그래프
- 가중치 / 비가중치
- 인접 리스트 기반 (대부분의 알고리즘에서 더 효율적)

주요 표현:
- Adjacency List: { vertex: [(neighbor, weight), ...], ... }
- Adjacency Matrix: 2차원 리스트 (V가 작을 때 유용, 여기서는 생략)

기본 연산:
- add_vertex, add_edge, remove_edge 등: O(1) 또는 O(degree)
- BFS, DFS: O(V + E)
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from collections import deque, defaultdict


class Graph:
    """
    범용 그래프 클래스
    """

    def __init__(self, directed: bool = False):
        self.directed = directed
        # vertex -> list of (neighbor, weight)
        self._adj: Dict[Any, List[Tuple[Any, float]]] = defaultdict(list)

    def add_vertex(self, v: Any) -> None:
        """ 정점 추가 (이미 있어도 무시)"""
        _ = self._adj[v]  # defaultdict이미로 자동 생성

    def add_edge(self, u: Any, v: Any, weight: float = 1.0) -> None:
        """ 간선 추가"""
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u].append((v, weight))
        if not self.directed:
            self._adj[v].append((u, weight))

    def remove_edge(self, u: Any, v: Any) -> None:
        """ 간선 제거 (첫 번째로 발견되는 것만)"""
        self._adj[u] = [(x, w) for x, w in self._adj[u] if x != v]
        if not self.directed:
            self._adj[v] = [(x, w) for x, w in self._adj[v] if x != u]

    def vertices(self) -> List[Any]:
        return list(self._adj.keys())

    def edges(self) -> List[Tuple[Any, Any, float]]:
        """ 모든 간선 반환 (무방향일 경우 중복 제거)"""
        seen = set()
        result = []
        for u in self._adj:
            for v, w in self._adj[u]:
                if self.directed:
                    result.append((u, v, w))
                else:
                    edge = tuple(sorted([u, v]))
                    if edge not in seen:
                        seen.add(edge)
                        result.append((u, v, w))
        return result

    def neighbors(self, v: Any) -> List[Tuple[Any, float]]:
        return self._adj.get(v, [])

    def has_vertex(self, v: Any) -> bool:
        return v in self._adj

    def __repr__(self) -> str:
        return f"Graph(directed={self.directed}, vertices={len(self._adj)})"

    # ==================== 기본 탐색 ====================

    def bfs(self, start: Any) -> List[Any]:
        """ 너비 우선 탐색 O(V+E)"""
        if start not in self._adj:
            return []
        visited: Set[Any] = set()
        order: List[Any] = []
        q: deque = deque([start])
        visited.add(start)

        while q:
            u = q.popleft()
            order.append(u)
            for v, _ in self._adj[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        return order

    def dfs(self, start: Any) -> List[Any]:
        """ 깊이 우선 탐색 (재귀) O(V+E)"""
        if start not in self._adj:
            return []
        visited: Set[Any] = set()
        order: List[Any] = []

        def _dfs(u: Any):
            visited.add(u)
            order.append(u)
            for v, _ in self._adj[u]:
                if v not in visited:
                    _dfs(v)

        _dfs(start)
        return order

    def dfs_iterative(self, start: Any) -> List[Any]:
        """ 스택을 이용한 반복 DFS"""
        if start not in self._adj:
            return []
        visited: Set[Any] = set()
        order: List[Any] = []
        stack = [start]

        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            order.append(u)
            # 역순으로 넣어서 원래 순서 유지 (선택)
            for v, _ in reversed(self._adj[u]):
                if v not in visited:
                    stack.append(v)
        return order

    # ==================== 연결 요소 ====================

    def connected_components(self) -> List[List[Any]]:
        """ 무방향 그래프의 연결 요소들"""
        if self.directed:
            raise ValueError("connected_components is for undirected graphs")

        visited: Set[Any] = set()
        components = []

        for v in self.vertices():
            if v not in visited:
                comp = self.dfs(v)
                components.append(comp)
                visited.update(comp)
        return components

    # ==================== 위상 정렬 (Directed Graph) ====================

    def topological_sort(self) -> List[Any]:
        """
        위상 정렬 (Kahn's algorithm - BFS 기반)
        사이클이 있으면 예외 발생
        """
        if not self.directed:
            raise ValueError("Topological sort only for directed graphs")

        # 진입 차수(indegree) 계산
        indegree: Dict[Any, int] = {v: 0 for v in self.vertices()}
        for u in self._adj:
            for v, _ in self._adj[u]:
                indegree[v] = indegree.get(v, 0) + 1

        q: deque = deque([v for v in indegree if indegree[v] == 0])
        order: List[Any] = []

        while q:
            u = q.popleft()
            order.append(u)
            for v, _ in self._adj[u]:
                indegree[v] -= 1
                if indegree[v] == 0:
                    q.append(v)

        if len(order) != len(indegree):
            raise ValueError("Graph has a cycle (no topological order)")

        return order


if __name__ == "__main__":
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("C", "D")
    g.add_edge("D", "E")

    print("BFS from A:", g.bfs("A"))
    print("DFS from A:", g.dfs("A"))
    print("Connected components:", g.connected_components())

    dg = Graph(directed=True)
    dg.add_edge("A", "B")
    dg.add_edge("A", "C")
    dg.add_edge("B", "D")
    dg.add_edge("C", "D")
    dg.add_edge("D", "E")
    print("Topological sort:", dg.topological_sort())