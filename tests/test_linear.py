import pytest
from linear.dynamic_array import DynamicArray
from linear.singly_linked_list import SinglyLinkedList
from linear.doubly_linked_list import DoublyLinkedList
from linear.stack import ArrayStack, LinkedStack
from linear.queue import CircularQueue, LinkedQueue


def test_dynamic_array_basic():
    arr = DynamicArray()
    for i in range(20):
        arr.append(i)
    assert len(arr) == 20
    assert arr[5] == 5
    assert arr.pop() == 19
    assert len(arr) == 19
    arr.insert(0, -1)
    assert arr[0] == -1
    assert arr.delete(0) == -1
    assert list(arr) == list(range(19))


def test_singly_linked_list():
    ll = SinglyLinkedList()
    ll.append(1)
    ll.append(2)
    ll.prepend(0)
    assert len(ll) == 3
    assert ll.to_list() == [0, 1, 2]
    assert ll.delete_head() == 0
    assert ll.delete_value(1) is True
    assert ll.to_list() == [2]


def test_doubly_linked_list():
    dll = DoublyLinkedList()
    dll.append("A")
    dll.append("B")
    dll.prepend("Z")
    assert dll.to_list() == ["Z", "A", "B"]
    assert dll.to_list_reversed() == ["B", "A", "Z"]
    dll.delete_value("A")
    assert dll.to_list() == ["Z", "B"]


def test_array_stack():
    s = ArrayStack()
    s.push(10)
    s.push(20)
    assert s.peek() == 20
    assert s.pop() == 20
    assert len(s) == 1


def test_linked_stack():
    s = LinkedStack()
    s.push("x")
    s.push("y")
    assert s.pop() == "y"
    assert s.peek() == "x"


def test_circular_queue():
    q = CircularQueue(4)
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.dequeue() == 1
    q.enqueue(4)
    q.enqueue(5)
    assert len(q) == 4
    with pytest.raises(OverflowError):
        q.enqueue(99)


def test_linked_queue():
    q = LinkedQueue()
    q.enqueue("first")
    q.enqueue("second")
    assert q.dequeue() == "first"
    assert q.front() == "second"