"""
Singly Linked List (단방향 연결 리스트)

개념:
- 각 노드가 data와 다음 노드를 가리키는 next 포인터만 가짐
- head (시작)만 알고 있으면 전체를 순회할 수 있음
- Tail을 별도로 관리하면 append를 O(1)로 만들 수 있음 (여기서는 tail도 관리)

주요 연산 복잡도 (tail 관리 기준):
- insert at head (prepend): O(1)
- append (tail에 추가): O(1)
- delete head: O(1)
- delete by value or at position: O(n) (이전 노드를 찾아야 함)
- access by index: O(n)
- search: O(n)

교육 포인트:
- 포인터(참조) 개념
- head/tail/null 처리
- dummy head (sentinel) 사용 여부
"""

from typing import Any, Optional, Iterator


class SinglyNode:
    """ 단방향 연결 리스트의 노드"""
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional["SinglyNode"] = None

    def __repr__(self) -> str:
        return f"SinglyNode({self.data})"


class SinglyLinkedList:
    """ 교육용 단방향 연결 리스트 (tail 관리 포함)"""

    def __init__(self):
        self.head: Optional[SinglyNode] = None
        self.tail: Optional[SinglyNode] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __repr__(self) -> str:
        return " -> ".join(str(x) for x in self) + " -> None"

    def is_empty(self) -> bool:
        return self.head is None

    def prepend(self, data: Any) -> None:
        """ 맨 앞에 삽입 O(1)"""
        new_node = SinglyNode(data)
        new_node.next = self.head
        self.head = new_node
        if self.tail is None:  # 처음 삽입
            self.tail = new_node
        self._size += 1

    def append(self, data: Any) -> None:
        """ 맨 뒤에 삽입 O(1) (tail 덕분)"""
        new_node = SinglyNode(data)
        if self.tail is None:  # 빈 리스트
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def insert_after(self, prev_node: SinglyNode, data: Any) -> None:
        """ 특정 노드 뒤에 삽입 O(1)"""
        if prev_node is None:
            raise ValueError("prev_node cannot be None")
        new_node = SinglyNode(data)
        new_node.next = prev_node.next
        prev_node.next = new_node
        if prev_node is self.tail:
            self.tail = new_node
        self._size += 1

    def delete_head(self) -> Any:
        """ 머리 노드 삭제 O(1)"""
        if self.head is None:
            raise IndexError("delete from empty list")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:  # 마지막 노드였음
            self.tail = None
        self._size -= 1
        return data

    def delete_tail(self) -> Any:
        """ 끼리 노드 삭제 O(n) — 이전 노드를 찾아야 함"""
        if self.head is None:
            raise IndexError("delete from empty list")
        if self.head is self.tail:  # 노드 1개
            data = self.head.data
            self.head = self.tail = None
            self._size -= 1
            return data

        current = self.head
        while current.next is not self.tail:
            current = current.next
        data = self.tail.data
        current.next = None
        self.tail = current
        self._size -= 1
        return data

    def delete_value(self, value: Any) -> bool:
        """
        값이 일치하는 첫 번째 노드 삭제 O(n)
        삭제 성공 시 True, 없으면 False
        """
        if self.head is None:
            return False

        if self.head.data == value:
            self.delete_head()
            return True

        prev = self.head
        current = self.head.next
        while current:
            if current.data == value:
                prev.next = current.next
                if current is self.tail:
                    self.tail = prev
                self._size -= 1
                return True
            prev = current
            current = current.next
        return False

    def find(self, value: Any) -> Optional[SinglyNode]:
        """ 값으로 노드 찾기 O(n). 없으면 None"""
        current = self.head
        while current:
            if current.data == value:
                return current
            current = current.next
        return None

    def get_at(self, index: int) -> Any:
        """0-based index로 값 반환 O(n)"""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next  # type: ignore
        return current.data  # type: ignore

    def to_list(self) -> list[Any]:
        return list(self)

    def clear(self) -> None:
        self.head = self.tail = None
        self._size = 0


if __name__ == "__main__":
    ll = SinglyLinkedList()
    ll.append(10)
    ll.append(20)
    ll.prepend(5)
    print(ll)                    # 5 -> 10 -> 20 -> None
    print("len:", len(ll))

    ll.delete_value(10)
    print("10 삭제 후:", ll)

    print("head 삭제:", ll.delete_head())
    print("최종:", ll)