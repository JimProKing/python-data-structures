"""
Queue (큐) - FIFO (First In First Out)

구현:
1. Array-based Queue (비효율적 버전) — 이해용
2. Circular Queue (원형 큐) — 실용적이고 중요!
3. Linked List-based Queue — head/tail 관리 시 enqueue/dequeue 모두 O(1)

주요 연산: enqueue, dequeue, front, is_empty → O(1)

교육 포인트:
- 선형 큐의 문제점 (front가 계속 이동하면서 공간 낭비)
- Circular Queue가 왜 필요한가 (모듈러 연산)
- Linked List 기반이 왜 편한가
- 실제 Python에서는 collections.deque를 사용 (양쪽 끝 O(1))
"""

from typing import Any, Optional
from .singly_linked_list import SinglyLinkedList


class ArrayQueue:
    """
    단순 배열 기반 큐 (비효율적 — front가 이동하면서 공간이 낭비됨)
    교육 목적으로만 사용
    """

    def __init__(self, capacity: int = 8):
        self._capacity = capacity
        self._data: list[Any] = [None] * capacity
        self._front = 0
        self._rear = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        if self.is_empty():
            return "ArrayQueue([])"
        items = []
        idx = self._front
        for _ in range(self._size):
            items.append(self._data[idx])
            idx = (idx + 1) % self._capacity
        return f"ArrayQueue({items})"

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self._capacity

    def enqueue(self, item: Any) -> None:
        if self.is_full():
            raise OverflowError("Queue is full")
        self._data[self._rear] = item
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return item

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._data[self._front]


class CircularQueue:
    """
    원형 큐 (Circular Queue) — 가장 실용적인 배열 기반 큐 구현

    핵심 아이디어:
    - rear = (rear + 1) % capacity
    - front = (front + 1) % capacity
    - 비어있는 상태와 가득 찬 상태를 구분하는 방법:
        A. size 변수를 따로 두는다 (여기서 채택)
        B. 한 칸을 항상 비워둔다 (rear + 1) % capacity == front
    """

    def __init__(self, capacity: int = 8):
        if capacity < 1:
            capacity = 1
        self._capacity = capacity
        self._data: list[Any] = [None] * capacity
        self._front = 0
        self._rear = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        if self.is_empty():
            return "CircularQueue([])"
        items = []
        idx = self._front
        for _ in range(self._size):
            items.append(self._data[idx])
            idx = (idx + 1) % self._capacity
        return f"CircularQueue({items}, front={self._front}, rear={self._rear})"

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self._capacity

    def enqueue(self, item: Any) -> None:
        if self.is_full():
            raise OverflowError("Queue is full")
        self._data[self._rear] = item
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return item

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._data[self._front]

    def clear(self) -> None:
        self._data = [None] * self._capacity
        self._front = self._rear = self._size = 0


class LinkedQueue:
    """
    Singly Linked List 기반 큐
    head에서 dequeue, tail에서 enqueue → 둘 다 O(1)
    """

    def __init__(self):
        self._list = SinglyLinkedList()

    def __len__(self) -> int:
        return len(self._list)

    def __repr__(self) -> str:
        return f"LinkedQueue({self._list.to_list()})"

    def is_empty(self) -> bool:
        return self._list.is_empty()

    def enqueue(self, item: Any) -> None:
        """O(1) — tail에 append"""
        self._list.append(item)

    def dequeue(self) -> Any:
        """O(1) — head 삭제"""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._list.delete_head()

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("front from empty queue")
        return self._list.head.data  # type: ignore

    def clear(self) -> None:
        self._list.clear()


# 기본 추천 구현은 CircularQueue
Queue = CircularQueue


if __name__ == "__main__":
    print("=== CircularQueue 데모 ===")
    q = CircularQueue(4)
    for i in range(3):
        q.enqueue(i)
    print(q)

    print("dequeue:", q.dequeue())
    print(q)

    q.enqueue(10)
    q.enqueue(20)
    print("가득 찼 을 때:", q, "full?", q.is_full())

    try:
        q.enqueue(99)
    except OverflowError as e:
        print("OverflowError:", e)

    print("=== LinkedQueue 데모 ===")
    lq = LinkedQueue()
    lq.enqueue("first")
    lq.enqueue("second")
    print(lq)
    print("dequeue:", lq.dequeue())
    print(lq)