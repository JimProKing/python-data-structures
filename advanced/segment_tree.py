"""
Segment Tree (세그먼트 트리) — 기본 구현

주로 다루는 용도:
- 구간 합 (Range Sum)
- 구간 최솏값 / 최댓값 (Range Min/Max Query)
- 구간 업데이트 + 쿼리

배열을 기반으로 완전 이진 트리 형태로 구성 (보통 4*N 크기 사용)

주요 연산:
- build: O(n)
- update (point update): O(log n)
- query (range query): O(log n)

교육 포인트:
- 1-based indexing 트리 vs 0-based 원본 배열
- left child = 2*node, right = 2*node+1
- 재귀적으로 구간을 나누고 합치는 구조
- Lazy Propagation은 고급 주제 (여기서는 기본 버전만)

이 구현은 Range Sum Query를 기본으로 함.
"""

from typing import List, Callable, Any


class SegmentTree:
    """
    기본 Segment Tree (Range Sum 기준)
    필요에 따라 min/max 등으로 쉽게 변경 가능
    """

    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2 * node, start, mid)
        self._build(arr, 2 * node + 1, mid + 1, end)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, idx: int, value: int) -> None:
        """idx 위치의 값을 value로 별경"""
        self._update(1, 0, self.n - 1, idx, value)

    def _update(self, node: int, start: int, end: int, idx: int, value: int) -> None:
        if start == end:
            self.tree[node] = value
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2 * node, start, mid, idx, value)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, value)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, left: int, right: int) -> int:
        """[left, right] 구간의 합 반환 (포함)"""
        if left > right:
            return 0
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        # 완전히 포함되지 않음
        if r < start or end < l:
            return 0
        # 완전히 포함됨
        if l <= start and end <= r:
            return self.tree[node]
        # 일부만 겹침 → 분할
        mid = (start + end) // 2
        left_sum = self._query(2 * node, start, mid, l, r)
        right_sum = self._query(2 * node + 1, mid + 1, end, l, r)
        return left_sum + right_sum


class SegmentTreeMin:
    """Range Minimum Query용 Segment Tree"""

    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2 * node, start, mid)
        self._build(arr, 2 * node + 1, mid + 1, end)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])

    def update(self, idx: int, value: int) -> None:
        self._update(1, 0, self.n - 1, idx, value)

    def _update(self, node: int, start: int, end: int, idx: int, value: int) -> None:
        if start == end:
            self.tree[node] = value
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2 * node, start, mid, idx, value)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, value)
        self.tree[node] = min(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, left: int, right: int) -> int:
        if left > right:
            return float("inf")
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return float("inf")
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return min(
            self._query(2 * node, start, mid, l, r),
            self._query(2 * node + 1, mid + 1, end, l, r),
        )


if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)
    print("초기 합 [0,5]:", st.query(0, 5))
    print("합 [1,3]:", st.query(1, 3))

    st.update(2, 100)  # 5 → 100
    print("업데이트 후 [1,3]:", st.query(1, 3))
    print("전체 합:", st.query(0, 5))

    print("\n=== Range Min ===")
    stm = SegmentTreeMin([4, 2, 7, 1, 9, 3])
    print("min [0,5]:", stm.query(0, 5))
    print("min [2,4]:", stm.query(2, 4))
    stm.update(3, 10)  # 1 → 10
    print("업데이트 후 min [0,3]:", stm.query(0, 3))