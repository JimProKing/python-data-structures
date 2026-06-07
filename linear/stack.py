"""
Stack (스택) - LIFO (Last In First Out)

구현 방식 2가지:
1. Array-based (Python list 사용) — 가장 실용적
2. Linked List-based — 연결 리스트로 구현 (교육용)

주요 연산: push, pop, peek, is_empty 모두 O(1)

교육 포인트:
- Call Stack, Undo, Backtracking, DFS 등에 사용
- Python에서는 list를 stack으로 바로 사용할 수 있음 (append/pop)
- 하지만 '직접 구현'해보는 것이 내부 동작 이해에 중요
"""

from typing import Any, Optional
from .singly_linked_list import SinglyLinkedList, SinglyNode


class ArrayStack:
    """Python list를 내부 저장소로 사용하는 스택 (추천 방식)"""

    def __init__(self):
        self._data: list[Any] = []

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"ArrayStack({self._data})"

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def push(self, item: Any) -> None:
        """O(1) amortized"""
        self._data.append(item)

    def pop(self) -> Any:
        """O(1) amortized"""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        """O(1)"""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def clear(self) -> None:
        self._data.clear()


class LinkedStack:
    """
    Singly Linked List를 사용한 스택 구현 (교육용)
    head 쪽에서 push/pop을 하면 모든 연산이 O(1)
    """

    def __init__(self):
        self._list = SinglyLinkedList()

    def __len__(self) -> int:
        return len(self._list)

    def __repr__(self) -> str:
        return f"LinkedStack({list(self._list)})"

    def is_empty(self) -> bool:
        return self._list.is_empty()

    def push(self, item: Any) -> None:
        """O(1) — head에 prepend"""
        self._list.prepend(item)

    def pop(self) -> Any:
        """O(1) — head 삭제"""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._list.delete_head()

    def peek(self) -> Any:
        """O(1)"""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._list.head.data  # type: ignore

    def clear(self) -> None:
        self._list.clear()


# 편의상 기본 스택은 ArrayStack으로 제공
Stack = ArrayStack


if __name__ == "__main__":
    print("=== ArrayStack ===")
    s = ArrayStack()
    s.push(1)
    s.push(2)
    s.push(3)
    print(s, "peek:", s.peek())
    print("pop:", s.pop())
    print(s)

    print("\n=== LinkedStack ===")
    ls = LinkedStack()
    ls.push("a")
    ls.push("b")
    print(ls)
    print("pop:", ls.pop())
    print(ls)