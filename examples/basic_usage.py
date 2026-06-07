"""
기본 사용 예시 모음

각 자료구조를 어떻게 쓰는지 간단히 보여줍니다.
실제 연습할 때는 각 모듈을 직접 열어서 코드를 읽고, practice/에서 직접 구현해보세요.

직접 실행: PYTHONPATH=. python examples/basic_usage.py   (Windows: $env:PYTHONPATH="."; python ...)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from linear.dynamic_array import DynamicArray
from linear.stack import Stack
from linear.queue import CircularQueue
from trees.binary_search_tree import BST
from trees.heap import MinHeap
from hash_tables.hash_table import HashTable
from graphs.graph import Graph
from graphs.graph_algorithms import dijkstra
from advanced.union_find import UnionFind


def demo_linear():
    print("=== Dynamic Array ===")
    arr = DynamicArray()
    for i in range(5):
        arr.append(i * 10)
    print(arr)
    arr.insert(2, 999)
    print("insert 후:", arr)

    print("\n=== Stack ===")
    s = Stack()
    for c in "abc":
        s.push(c)
    while not s.is_empty():
        print(s.pop(), end=" ")
    print()


def demo_tree():
    print("\n=== BST ===")
    bst = BST()
    bst.insert_many([50, 30, 70, 20, 40, 60])
    print("Inorder:", bst.inorder())
    print("kth smallest(4):", bst.kth_smallest(4))


def demo_graph():
    print("\n=== Graph + Dijkstra ===")
    g = Graph(directed=False)
    g.add_edge("서울", "대전", 140)
    g.add_edge("서울", "인천", 30)
    g.add_edge("대전", "대구", 120)
    g.add_edge("인천", "대구", 200)

    dist, _ = dijkstra(g, "서울")
    print("서울 기준 최단 거리:", dist)


def demo_advanced():
    print("\n=== UnionFind ===")
    uf = UnionFind(["A", "B", "C", "D"])
    uf.union("A", "B")
    uf.union("C", "D")
    print("A와 B 연결?", uf.connected("A", "B"))
    print("A와 C 연결?", uf.connected("A", "C"))


if __name__ == "__main__":
    demo_linear()
    demo_tree()
    demo_graph()
    demo_advanced()
    print("\n모두 성공적으로 실행되었습니다!")