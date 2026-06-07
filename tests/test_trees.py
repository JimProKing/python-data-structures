import pytest
from trees.binary_search_tree import BST
from trees.avl_tree import AVLTree
from trees.heap import MinHeap, MaxHeap, heap_sort
from trees.trie import Trie


def test_bst_basic():
    bst = BST()
    bst.insert_many([50, 30, 70, 20, 40])
    assert bst.inorder() == [20, 30, 40, 50, 70]
    assert bst.contains(30)
    assert not bst.contains(99)
    assert bst.min() == 20
    assert bst.max() == 70
    assert bst.kth_smallest(3) == 40
    bst.delete(30)
    assert bst.inorder() == [20, 40, 50, 70]


def test_avl_balancing():
    avl = AVLTree()
    for i in range(1, 8):
        avl.insert(i)
    assert avl.is_balanced()
    assert avl.height() <= 3  # log n 수준


def test_min_heap():
    h = MinHeap()
    for x in [5, 3, 8, 1, 2]:
        h.insert(x)
    assert h.extract_min() == 1
    assert h.extract_min() == 2


def test_max_heap():
    h = MaxHeap()
    h.build_heap([1, 5, 3, 9, 2])
    assert h.extract_max() == 9


def test_heap_sort():
    data = [3, 1, 4, 1, 5, 9, 2]
    assert heap_sort(data[:]) == sorted(data)
    assert heap_sort(data[:], reverse=True) == sorted(data, reverse=True)


def test_trie():
    t = Trie()
    for w in ["apple", "app", "apricot", "banana"]:
        t.insert(w)
    assert t.search("app")
    assert not t.search("appl")
    assert t.starts_with("ap")
    assert t.get_words_with_prefix("ap") == ["app", "apple", "apricot"]
    t.delete("app")
    assert not t.search("app")
    assert t.search("apple")  # 여전히 존재해야 함