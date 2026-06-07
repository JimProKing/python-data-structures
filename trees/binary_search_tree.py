"""
Binary Search Tree (BST, 이진 탐색 트리)

특징:
- 왼쪽 서브트리 모든 값 < 노드 값
- 오른쪽 서브트리 모든 값 > 노드 값
- Inorder 순회 시 정렬된 순서로 방문됨

주요 연산 복잡도:
- insert, search, delete: O(log n) 평균, O(n) 최악 (편향된 경우)
- 최악의 경우를 막기 위해 → AVL, Red-Black Tree 사용

교육 포인트:
- delete에서 3가지 경우 (자식 0, 1, 2개)
- 자식이 2개일 때 successor (또는 predecessor) 찾는 방법
- min/max, floor/ceil, kth smallest 등 파생 연산
"""

from typing import Any, Optional, List
from .binary_tree import TreeNode, BinaryTree


class BST(BinaryTree):
    """ 이진 탐색 트리 (표준 구현)"""

    def __init__(self):
        super().__init__()

    # ==================== 검색 ====================

    def search(self, key: Any) -> Optional[TreeNode]:
        """O(log n) 평균"""
        current = self.root
        while current:
            if key == current.data:
                return current
            elif key < current.data:
                current = current.left
            else:
                current = current.right
        return None

    def contains(self, key: Any) -> bool:
        return self.search(key) is not None

    # ==================== 삽입 ====================

    def insert(self, key: Any) -> None:
        """O(log n) 평균"""
        if self.root is None:
            self.root = TreeNode(key)
            return

        current = self.root
        while True:
            if key < current.data:
                if current.left is None:
                    current.left = TreeNode(key)
                    return
                current = current.left
            elif key > current.data:
                if current.right is None:
                    current.right = TreeNode(key)
                    return
                current = current.right
            else:
                # 중복 허용 안 함 (필요하면 카운트 방식으로 변경)
                return

    # 재귀 버전 (더 깔끔하고 많이 쓰임)
    def insert_recursive(self, key: Any) -> None:
        def _insert(node: Optional[TreeNode], key: Any) -> TreeNode:
            if node is None:
                return TreeNode(key)
            if key < node.data:
                node.left = _insert(node.left, key)
            elif key > node.data:
                node.right = _insert(node.right, key)
            # 중복은 무시
            return node

        self.root = _insert(self.root, key)

    # ==================== 삭제 (가장 중요) ====================

    def delete(self, key: Any) -> bool:
        """
        삭제 성공 시 True 반환
        3가지 경우 처리:
        1. 자식 없음 → 그냥 삭제
        2. 자식 1개 → 그 자식으로 대체
        3. 자식 2개 → inorder successor(오른쪽 서브트리의 최소값)로 대체
        """
        self.root, deleted = self._delete_recursive(self.root, key)
        return deleted

    def _delete_recursive(self, node: Optional[TreeNode], key: Any) -> tuple[Optional[TreeNode], bool]:
        if node is None:
            return None, False

        if key < node.data:
            node.left, deleted = self._delete_recursive(node.left, key)
            return node, deleted
        elif key > node.data:
            node.right, deleted = self._delete_recursive(node.right, key)
            return node, deleted
        else:
            # 삭제할 노드 찾음
            # case 1 & 2: 자식 0개 또는 1개
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            # case 3: 자식 2개 → 오른쪽 서브트리에서 최소값 찾기 (inorder successor)
            successor = self._find_min_node(node.right)
            node.data = successor.data
            # successor 삭제 (오른쪽 서브트리에서)
            node.right, _ = self._delete_recursive(node.right, successor.data)
            return node, True

    def _find_min_node(self, node: TreeNode) -> TreeNode:
        while node.left:
            node = node.left
        return node

    # ==================== 유틸리티 ====================

    def min(self) -> Any:
        if self.root is None:
            raise ValueError("Tree is empty")
        node = self.root
        while node.left:
            node = node.left
        return node.data

    def max(self) -> Any:
        if self.root is None:
            raise ValueError("Tree is empty")
        node = self.root
        while node.right:
            node = node.right
        return node.data

    def kth_smallest(self, k: int) -> Any:
        """
        Inorder 순회하면서 k번째 작은 값 찾기 (1-based)
        O(k) ~ O(n)
        """
        if k < 1:
            raise ValueError("k must be >= 1")

        count = [0]
        result = [None]

        def _inorder(node: Optional[TreeNode]) -> bool:
            if node is None:
                return False
            if _inorder(node.left):
                return True
            count[0] += 1
            if count[0] == k:
                result[0] = node.data
                return True
            return _inorder(node.right)

        _inorder(self.root)
        if result[0] is None:
            raise IndexError(f"Tree has fewer than {k} elements")
        return result[0]

    # 편의 메서드
    def insert_many(self, keys: List[Any]) -> None:
        for k in keys:
            self.insert(k)


if __name__ == "__main__":
    bst = BST()
    values = [50, 30, 70, 20, 40, 60, 80, 10]
    bst.insert_many(values)

    print("Inorder (정렬되어야 함):", bst.inorder())
    print("Preorder :", bst.preorder())
    print("Min:", bst.min(), "Max:", bst.max())
    print("3rd smallest:", bst.kth_smallest(3))

    print("40 검색:", bst.contains(40))
    print("99 검색:", bst.contains(99))

    print("삭제 30:", bst.delete(30))
    print("삭제 후 Inorder:", bst.inorder())

    print("삭제 50 (root):", bst.delete(50))
    print("삭제 후 Inorder:", bst.inorder())