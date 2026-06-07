"""
Doubly Linked List (양방향 연결 리스트)

개념:
- 각 노드가 prev와 next 포인터를 모두 가짐
- head와 tail을 모두 관리하면 양쪽 끝 연산이 모두 O(1)
- 중간 삭제/삽입 시 이전 노드를 알 필요가 없어 더 편리함

주요 연산 복잡도 (head + tail 관리 시):
- prepend / append: O(1)
- delete head / tail: O(1)
- insert / delete at arbitrary position: O(n) (노드 찾는 데 O(n))
- 하지만 "이미 해당 노드의 참조를 알고 있다면" insert/delete는 O(1)

교육 포인트:
- sentinel (더미 head/tail) 사용 시 경계 조건이 훨씬 단순해짐
- 여기서는 sentinel 없이 명시적으로 구현 (대학 과정에서 흔한 방식)
"""

from typing import Any, Optional, Iterator


class DoublyNode:
    """ 양방향 연결 리스트 노드"""
    def __init__(self, data: Any):
        self.data = data
        self.prev: Optional["DoublyNode"] = None
        self.next: Optional["DoublyNode"] = None

    def __repr__(self) -> str:
        return f"DoublyNode({self.data})"


class DoublyLinkedList:
    """ 교육용 양방향 연결 리스트"""

    def __init__(self):
        self.head: Optional[DoublyNode] = None
        self.tail: Optional[DoublyNode] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __reversed__(self) -> Iterator[Any]:
        current = self.tail
        while current:
            yield current.data
            current = current.prev

    def __repr__(self) -> str:
        return " <-> ".join(str(x) for x in self) + " <-> None"

    def is_empty(self) -> bool:
        return self.head is None

    def prepend(self, data: Any) -> None:
        """O(1)"""
        new_node = DoublyNode(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def append(self, data: Any) -> None:
        """O(1)"""
        new_node = DoublyNode(data)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def insert_after(self, node: DoublyNode, data: Any) -> None:
        """ 특정 노드 뒤에 삽입 O(1)"""
        if node is None:
            raise ValueError("node cannot be None")
        new_node = DoublyNode(data)
        new_node.prev = node
        new_node.next = node.next

        if node.next:
            node.next.prev = new_node
        else:
            self.tail = new_node  # node가 tail이었음

        node.next = new_node
        self._size += 1

    def insert_before(self, node: DoublyNode, data: Any) -> None:
        """ 특정 노드 앞에 삽입 O(1)"""
        if node is None:
            raise ValueError("node cannot be None")
        new_node = DoublyNode(data)
        new_node.next = node
        new_node.prev = node.prev

        if node.prev:
            node.prev.next = new_node
        else:
            self.head = new_node  # node가 head이었음

        node.prev = new_node
        self._size += 1

    def delete_node(self, node: DoublyNode) -> Any:
        """
        주어진 노드를 삭제 O(1) (이미 노드 참조를 알고 있을 때)
        """
        if node is None:
            raise ValueError("Cannot delete None node")

        data = node.data

        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        self._size -= 1
        return data

    def delete_head(self) -> Any:
        """O(1)"""
        if self.head is None:
            raise IndexError("delete from empty list")
        return self.delete_node(self.head)

    def delete_tail(self) -> Any:
        """O(1)"""
        if self.tail is None:
            raise IndexError("delete from empty list")
        return self.delete_node(self.tail)

    def delete_value(self, value: Any) -> bool:
        """ 값으로 첫 번째 노드 삭제 O(n)"""
        current = self.head
        while current:
            if current.data == value:
                self.delete_node(current)
                return True
            current = current.next
        return False

    def find(self, value: Any) -> Optional[DoublyNode]:
        """O(n)"""
        current = self.head
        while current:
            if current.data == value:
                return current
            current = current.next
        return None

    def get_at(self, index: int) -> Any:
        """O(n)"""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next  # type: ignore
        return current.data  # type: ignore

    def to_list(self) -> list[Any]:
        return list(self)

    def to_list_reversed(self) -> list[Any]:
        return list(reversed(self))

    def clear(self) -> None:
        self.head = self.tail = None
        self._size = 0


if __name__ == "__main__":
    dll = DoublyLinkedList()
    dll.append("A")
    dll.append("B")
    dll.prepend("Z")
    print(dll)                    # Z <-> A <-> B <-> None
    print("역방향:", dll.to_list_reversed())

    node_a = dll.find("A")
    if node_a:
        dll.insert_after(node_a, "A+")
    print("A 뒤에 A+ 삽입:", dll)

    dll.delete_value("A")
    print("A 삭제 후:", dll)