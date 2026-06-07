"""
Binary Tree (이진 트리) + 순회(Traversal)

개념:
- 각 노드가 최대 2개의 자식(left, right)을 가짐
- 이진 트리 자체는 '정렬'된 구조가 아님 (BST가 정렬된 버전)

주요 순회 방법 (매우 중요!):
1. Preorder  (전위): Root → Left → Right
2. Inorder   (중위): Left → Root → Right   ← BST에서 정렬 순서
3. Postorder (후위): Left → Right → Root
4. Level Order (BFS): 위 → 아래, 왼쪽 → 오른쪽

모든 순회는 O(n)

교육 포인트:
- 재귀 vs 반복(스택 사용) 구현
- Inorder가 BST에서 정렬된 순서를 주는 이유
- Level Order는 Queue를 사용
"""

from typing import Any, Optional, List, Callable
from collections import deque


class TreeNode:
    """ 이진 트리 노드"""
    def __init__(self, data: Any):
        self.data = data
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None

    def __repr__(self) -> str:
        return f"TreeNode({self.data})"


class BinaryTree:
    """
    기본 이진 트리 (구조만 관리)
    실제로는 BST, AVL, Heap 등에서 상속하거나 사용됨
    """

    def __init__(self):
        self.root: Optional[TreeNode] = None

    def is_empty(self) -> bool:
        return self.root is None

    # ==================== 재귀 순회 ====================

    def preorder(self) -> List[Any]:
        """ 전위 순회: Root → Left → Right"""
        result: List[Any] = []

        def _pre(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            result.append(node.data)
            _pre(node.left)
            _pre(node.right)

        _pre(self.root)
        return result

    def inorder(self) -> List[Any]:
        """ 중위 순회: Left → Root → Right"""
        result: List[Any] = []

        def _in(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            _in(node.left)
            result.append(node.data)
            _in(node.right)

        _in(self.root)
        return result

    def postorder(self) -> List[Any]:
        """ 후위 순회: Left → Right → Root"""
        result: List[Any] = []

        def _post(node: Optional[TreeNode]) -> None:
            if node is None:
                return
            _post(node.left)
            _post(node.right)
            result.append(node.data)

        _post(self.root)
        return result

    # ==================== 반복(Iterative) 순회 ====================

    def preorder_iterative(self) -> List[Any]:
        """ 스택을 사용한 전위 순회"""
        if self.root is None:
            return []
        result: List[Any] = []
        stack: List[TreeNode] = [self.root]
        while stack:
            node = stack.pop()
            result.append(node.data)
            # right를 먼저 넣어야 left가 먼저 처리됨
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result

    def inorder_iterative(self) -> List[Any]:
        """ 스택을 사용한 중위 순회 (가장 많이 나오는 패턴)"""
        result: List[Any] = []
        stack: List[TreeNode] = []
        current = self.root

        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.data)
            current = current.right
        return result

    def postorder_iterative(self) -> List[Any]:
        """ 두 개의 스택 또는 하나의 스택 + visited 방식"""
        if self.root is None:
            return []
        result: List[Any] = []
        stack1: List[TreeNode] = [self.root]
        stack2: List[TreeNode] = []

        while stack1:
            node = stack1.pop()
            stack2.append(node)
            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)

        while stack2:
            result.append(stack2.pop().data)
        return result

    def level_order(self) -> List[Any]:
        """ 레벨 순서 순회 (BFS) — Queue 사용"""
        if self.root is None:
            return []
        result: List[Any] = []
        q: deque[TreeNode] = deque([self.root])
        while q:
            node = q.popleft()
            result.append(node.data)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        return result

    def height(self) -> int:
        """ 트리의 높이 (root에서 가장 먼 리프까지의 간선 수)"""

        def _height(node: Optional[TreeNode]) -> int:
            if node is None:
                return -1  # 리프의 높이는 0이 아니라, null의 높이를 -1로 보는 게 일반적
            return 1 + max(_height(node.left), _height(node.right))

        return _height(self.root)

    def size(self) -> int:
        """ 노드 개수"""

        def _size(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            return 1 + _size(node.left) + _size(node.right)

        return _size(self.root)

    def __repr__(self) -> str:
        return f"BinaryTree(root={self.root.data if self.root else None})"


# 간단한 수동 트리 생성 헬퍼 (테스트용)
def build_example_tree() -> BinaryTree:
    """
    예시 트리 생성:
            1
          /   \\
         2     3
        / \\   / \\
       4   5 6   7
    """
    tree = BinaryTree()
    tree.root = TreeNode(1)
    tree.root.left = TreeNode(2)
    tree.root.right = TreeNode(3)
    tree.root.left.left = TreeNode(4)
    tree.root.left.right = TreeNode(5)
    tree.root.right.left = TreeNode(6)
    tree.root.right.right = TreeNode(7)
    return tree


if __name__ == "__main__":
    tree = build_example_tree()
    print("Preorder :", tree.preorder())
    print("Inorder  :", tree.inorder())
    print("Postorder:", tree.postorder())
    print("LevelOrder:", tree.level_order())
    print("Iterative Preorder :", tree.preorder_iterative())
    print("Iterative Inorder  :", tree.inorder_iterative())
    print("Height:", tree.height(), "Size:", tree.size())