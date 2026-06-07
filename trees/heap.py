"""
Heap (힙) — 주로 Binary Heap

구현:
- Min-Heap (부모 <= 자식)
- Max-Heap (부모 >= 자식)

배열 표현 (가장 중요!):
- 부모 인덱스 i의 자식: left = 2*i + 1, right = 2*i + 2
- 자식 인덱스 j의 부모: (j - 1) // 2
- 0-based indexing 사용

주요 연산:
- insert: O(log n)  (heapify-up / bubble-up)
- extract_min / extract_max: O(log n)  (heapify-down / bubble-down)
- peek: O(1)
- build_heap: O(n)  (중요! from array)

교육 포인트:
- 완전 이진 트리 (Complete Binary Tree) 여야 함
- heapify-up vs heapify-down
- HeapSort의 원리 (extract를 n번 하면 정렬됨)
- Priority Queue의 기반 자료구조
"""

from typing import Any, List, Optional, Callable


class MinHeap:
    """Min-Heap (최소 힙) — extract 시 가장 작은 값이 나옴"""

    def __init__(self):
        self._data: List[Any] = []

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"MinHeap({self._data})"

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self._data[0]

    # ==================== Heapify ====================

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _heapify_up(self, i: int) -> None:
        """ 삽입 후 위로 올리기"""
        while i > 0:
            p = self._parent(i)
            if self._data[i] < self._data[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def _heapify_down(self, i: int) -> None:
        """extract 후 아래로 내리기"""
        n = len(self._data)
        while True:
            left = self._left(i)
            right = self._right(i)
            smallest = i

            if left < n and self._data[left] < self._data[smallest]:
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:
                smallest = right

            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    # ==================== 공개 API ====================

    def insert(self, value: Any) -> None:
        """O(log n)"""
        self._data.append(value)
        self._heapify_up(len(self._data) - 1)

    def extract_min(self) -> Any:
        """O(log n)"""
        if self.is_empty():
            raise IndexError("extract_min from empty heap")
        if len(self._data) == 1:
            return self._data.pop()

        min_val = self._data[0]
        self._data[0] = self._data.pop()  # 마지막 원소를 root로
        self._heapify_down(0)
        return min_val

    def build_heap(self, arr: List[Any]) -> None:
        """
        주어진 배열로부터 O(n) 시간에 힙 구성
        (n번 insert 하는 것보다 훨씬 효율적)
        """
        self._data = arr[:]
        n = len(self._data)
        # 가장 마지막 non-leaf 노드부터 heapify_down
        for i in range((n - 2) // 2, -1, -1):
            self._heapify_down(i)


class MaxHeap:
    """Max-Heap (최대 힙)"""

    def __init__(self):
        self._data: List[Any] = []

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"MaxHeap({self._data})"

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self._data[0]

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _heapify_up(self, i: int) -> None:
        while i > 0:
            p = self._parent(i)
            if self._data[i] > self._data[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def _heapify_down(self, i: int) -> None:
        n = len(self._data)
        while True:
            left = self._left(i)
            right = self._right(i)
            largest = i

            if left < n and self._data[left] > self._data[largest]:
                largest = left
            if right < n and self._data[right] > self._data[largest]:
                largest = right

            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break

    def insert(self, value: Any) -> None:
        self._data.append(value)
        self._heapify_up(len(self._data) - 1)

    def extract_max(self) -> Any:
        if self.is_empty():
            raise IndexError("extract_max from empty heap")
        if len(self._data) == 1:
            return self._data.pop()

        max_val = self._data[0]
        self._data[0] = self._data.pop()
        self._heapify_down(0)
        return max_val

    def build_heap(self, arr: List[Any]) -> None:
        self._data = arr[:]
        n = len(self._data)
        for i in range((n - 2) // 2, -1, -1):
            self._heapify_down(i)


def heap_sort(arr: List[Any], reverse: bool = False) -> List[Any]:
    """
    Heap을 이용한 정렬 (in-place가 아닌 버전)
    MinHeap 사용 시 오름차순, MaxHeap 사용 시 내림차순
    """
    if not arr:
        return []

    if reverse:
        h = MaxHeap()
    else:
        h = MinHeap()

    h.build_heap(arr)
    result = []
    extract = h.extract_max if reverse else h.extract_min

    while not h.is_empty():
        result.append(extract())
    return result


if __name__ == "__main__":
    print("=== MinHeap ===")
    h = MinHeap()
    for v in [10, 4, 15, 1, 7, 20]:
        h.insert(v)
        print(f"insert {v} -> {h}")

    print("extract_min sequence:")
    while not h.is_empty():
        print(h.extract_min(), end=" ")
    print()

    print("\n=== HeapSort ===")
    data = [3, 1, 4, 1, 5, 9, 2]
    print("원본:", data)
    print("오름차순:", heap_sort(data[:]))
    print("내림차순:", heap_sort(data[:], reverse=True))

    print("\n=== build_heap O(n) ===")
    h2 = MinHeap()
    h2.build_heap([9, 5, 3, 8, 1, 4, 7])
    print(h2)
    print("extract_min:", h2.extract_min())