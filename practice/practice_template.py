"""
직접 구현 연습용 템플릿

사용 방법:
1. 이 파일을 복사해서 `my_linked_list.py`, `my_bst.py` 등으로 만드세요.
2. 아래 클래스들을 직접 처음부터 끝까지 구현해보세요.
3. tests/ 폴더의 테스트를 돌려서 검증하세요.

예:
    pytest tests/test_linear.py::test_singly_linked_list -s
"""

from typing import Any, Optional, List


# ==================== 예시: 직접 Singly Linked List 구현해보기 ====================

class MySinglyNode:
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional["MySinglyNode"] = None


class MySinglyLinkedList:
    """TODO: 직접 구현해보세요!"""

    def __init__(self):
        self.head: Optional[MySinglyNode] = None
        self.tail: Optional[MySinglyNode] = None
        self._size = 0

    def append(self, data: Any) -> None:
        raise NotImplementedError

    def prepend(self, data: Any) -> None:
        raise NotImplementedError

    def delete_value(self, value: Any) -> bool:
        raise NotImplementedError

    def to_list(self) -> List[Any]:
        raise NotImplementedError

    # ... 필요한 메서드 더 추가


# ==================== 연습 문제 아이디어 ====================

"""
추가로 연습해볼 만한 것들 (자유롭게 구현):

1. Circular Linked List
2. Stack을 이용한 괄호 검사, 후위 표기법 계산기
3. Queue를 이용한 Josephus 문제
4. BST에 size, height, is_balanced (간단 버전) 추가
5. AVL delete 완성 (이미 되어 있음)
6. HashTable에 load factor, resize 로직 직접 작성
7. Graph에서 cycle detection (DFS)
8. Dijkstra를 PriorityQueue가 아닌 단순 리스트로 구현해보기 (비효율 버전)
9. Segment Tree에 Lazy Propagation 추가 (고급)
10. Disjoint Set에 size 기반 union 구현
"""


if __name__ == "__main__":
    print("이 파일은 연습용입니다. 직접 코드를 작성해보세요!")
    # ll = MySinglyLinkedList()
    # ll.append(1)
    # print(ll.to_list())