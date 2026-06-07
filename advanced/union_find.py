"""
Union-Find (Disjoint Set Union, DSU)

대학 과정에서 가장 실용적인 자료구조 중 하나.

핵심 최적화 2가지:
1. Union by Rank (또는 Size)
2. Path Compression (경로 압축)

이 두 가지를 모두 적용하면 거의 O(1) (Ackermann 함수 역함수) 성능이 나옴.

주요 연산:
- find(x): x가 속한 집합의 대표(root) 찾기
- union(x, y): 두 집합을 합치기
- connected(x, y): 같은 집합인지 확인

응용:
- Kruskal MST
- 네트워크 연결 여부
- 사이클 검출
- 이미지 처리 (connected component)
"""

from typing import Any, Dict, List


class UnionFind:
    """Path Compression + Union by Rank 최적화된 Union-Find"""

    def __init__(self, elements: List[Any] = None):
        self.parent: Dict[Any, Any] = {}
        self.rank: Dict[Any, int] = {}
        if elements:
            for e in elements:
                self.add(e)

    def add(self, x: Any) -> None:
        """ 새로운 원소 추가"""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x: Any) -> Any:
        """ 경로 압축(Path Compression) 적용"""
        if x not in self.parent:
            self.add(x)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 경로 압축
        return self.parent[x]

    def union(self, x: Any, y: Any) -> bool:
        """
        Union by Rank
        합쳐졌으면 True, 이미 같은 집합이면 False
        """
        px = self.find(x)
        py = self.find(y)
        if px == py:
            return False

        # rank가 낮은 쪽을 높은 쪽 밑으로
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1
        return True

    def connected(self, x: Any, y: Any) -> bool:
        return self.find(x) == self.find(y)

    def components(self) -> Dict[Any, List[Any]]:
        """ 현재 집합 구성 반환 (디버깅/테스트용)"""
        groups: Dict[Any, List[Any]] = {}
        for x in self.parent:
            root = self.find(x)
            groups.setdefault(root, []).append(x)
        return groups

    def count_components(self) -> int:
        return len(set(self.find(x) for x in self.parent))


# 별칭
DSU = UnionFind


if __name__ == "__main__":
    uf = UnionFind([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(4, 5)
    uf.union(6, 7)
    uf.union(0, 2)  # 0-1-2-3 연결
    uf.union(4, 6)  # 4-5-6-7 연결

    print("0과 3 연결?", uf.connected(0, 3))
    print("0과 5 연결?", uf.connected(0, 5))
    print("컴포넌트 수:", uf.count_components())
    print("컴포넌트 구성:", uf.components())

    uf.union(3, 7)  # 큰 두 집합 합치기
    print("합친 후 컴포넌트 수:", uf.count_components())