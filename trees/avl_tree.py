"""
AVL Tree (Adelson-Velsky and Landis Tree)

특징:
- 모든 노드의 Balance Factor |BF| <= 1 을 유지
- Balance Factor = height(left) - height(right)
- 회전(Rotation)을 통해 균형을 유지

회전 4가지 (LL, RR, LR, RL):
- LL (Left-Left): 오른쪽 회전 (single right rotation)
- RR (Right-Right): 왼쪽 회전 (single left rotation)
- LR (Left-Right): 왼쪽 회전 후 오른쪽 회전
- RL (Right-Left): 오른쪽 회전 후 왼쪽 회전

교육 포인트:
- 회전의 정확한 이해가 가장 중요 (그림을 그려가며 공부)
- 높이(height) 캐싱 (없으면 O(n) 비용 발생)
- BST의 모든 특성을 유지하면서 높이를 O(log n)으로 보장
- insert/delete 모두 O(log n) 보장
"""

from typing import Any, Optional, Tuple
from .binary_tree import TreeNode


class AVLNode(TreeNode):
    """AVL 트리용 노드 (높이 정보 포함)"""
    def __init__(self, data: Any):
        super().__init__(data)
        self.height: int = 1  # 리프의 높이는 1


class AVLTree:
    """AVL 트리 (자기 균형 이진 탐색 트리)"""

    def __init__(self):
        self.root: Optional[AVLNode] = None

    # ==================== 높이 / 균형 관련 ====================

    def _height(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node: AVLNode) -> int:
        return self._height(node.left) - self._height(node.right)

    # ==================== 회전 ====================

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """
        오른쪽 회전 (LL imbalance 해결)
        y의 왼쪽 자식 x가 y의 부모가 됨
        """
        x = y.left
        T2 = x.right

        # 회전
        x.right = y
        y.left = T2

        # 높이 갱신 (아래부터)
        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """
        왼쪽 회전 (RR imbalance 해결)
        x의 오른쪽 자식 y가 x의 부모가 됨
        """
        y = x.right
        T2 = y.left

        # 회전
        y.left = x
        x.right = T2

        self._update_height(x)
        self._update_height(y)

        return y

    # ==================== 삽입 ====================

    def insert(self, key: Any) -> None:
        self.root = self._insert(self.root, key)

    def _insert(self, node: Optional[AVLNode], key: Any) -> AVLNode:
        # 1. 일반 BST 삽입
        if node is None:
            return AVLNode(key)

        if key < node.data:
            node.left = self._insert(node.left, key)
        elif key > node.data:
            node.right = self._insert(node.right, key)
        else:
            return node  # 중복 무시

        # 2. 높이 갱신
        self._update_height(node)

        # 3. 균형 맞추기
        balance = self._balance_factor(node)

        # LL
        if balance > 1 and key < node.left.data:
            return self._rotate_right(node)

        # RR
        if balance < -1 and key > node.right.data:
            return self._rotate_left(node)

        # LR
        if balance > 1 and key > node.left.data:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # RL
        if balance < -1 and key < node.right.data:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    # ==================== 삭제 ====================

    def delete(self, key: Any) -> bool:
        self.root, deleted = self._delete(self.root, key)
        return deleted

    def _delete(self, node: Optional[AVLNode], key: Any) -> Tuple[Optional[AVLNode], bool]:
        if node is None:
            return None, False

        if key < node.data:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.data:
            node.right, deleted = self._delete(node.right, key)
        else:
            # 삭제할 노드
            if node.left is None:
                return node.right, True
            if node.right is None:
                return node.left, True

            # 두 자식 모두 있음 → 오른쪽 최소값
            successor = self._find_min(node.right)
            node.data = successor.data
            node.right, _ = self._delete(node.right, successor.data)
            deleted = True

        if node is None:
            return None, deleted

        # 높이 갱신 + 재균형
        self._update_height(node)
        balance = self._balance_factor(node)

        # LL
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node), deleted
        # LR
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node), deleted
        # RR
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node), deleted
        # RL
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node), deleted

        return node, deleted

    def _find_min(self, node: AVLNode) -> AVLNode:
        while node.left:
            node = node.left
        return node

    # ==================== 검색 ====================

    def search(self, key: Any) -> Optional[AVLNode]:
        current = self.root
        while current:
            if key == current.data:
                return current
            current = current.left if key < current.data else current.right
        return None

    def contains(self, key: Any) -> bool:
        return self.search(key) is not None

    # ==================== 순회 (BinaryTree와 유사) ====================

    def inorder(self) -> list[Any]:
        result = []

        def _in(node: Optional[AVLNode]):
            if node:
                _in(node.left)
                result.append(node.data)
                _in(node.right)

        _in(self.root)
        return result

    def height(self) -> int:
        return self._height(self.root)

    def is_balanced(self) -> bool:
        """ 모든 노드의 |BF| <= 1 인지 확인 (디버깅용)"""
        def check(node: Optional[AVLNode]) -> bool:
            if node is None:
                return True
            if abs(self._balance_factor(node)) > 1:
                return False
            return check(node.left) and check(node.right)
        return check(self.root)


if __name__ == "__main__":
    avl = AVLTree()
    values = [10, 20, 30, 40, 50, 25]  # 고의로 편향 유발
    for v in values:
        avl.insert(v)
        print(f"After insert {v}: inorder={avl.inorder()}, height={avl.height()}, balanced={avl.is_balanced()}")

    print("\n최종 Inorder:", avl.inorder())
    print("30 삭제:", avl.delete(30))
    print("삭제 후:", avl.inorder(), "balanced?", avl.is_balanced())