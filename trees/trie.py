"""
Trie (Prefix Tree, 또는 Digital Tree)

특징:
- 문자열 집합을 저장하고 빠르게 검색/접두사 검색
- 각 노드는 문자(char)를 key로 하는 자식 딕셔너리를 가짐
- 단어의 끝을 표시하는 is_end_of_word 플래그 필요

주요 연산:
- insert(word): O(L) L = 단어 길이
- search(word): O(L)
- starts_with(prefix): O(L) — 해당 prefix로 시작하는 단어가 있는지

응용:
- 자동 완성(Auto-complete)
- 스펠링 체크
- IP 라우팅 테이블
- 연관 검색어

교육 포인트:
- 공간 효율 (공통 접두사를 공유)
- vs HashSet: prefix 검색이 Trie만 가능
"""

from typing import Dict, List, Optional


class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end_of_word: bool = False


class Trie:
    """Trie (접두사 트리)"""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """O(L)"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """O(L) — 정확히 일치하는 단어가 있는지"""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """O(L) — 이 prefix로 시작하는 단어가 하나라도 있는지"""
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """ 주어진 prefix로 시작하는 모든 단어 반환 (DFS)"""
        node = self._find_node(prefix)
        if node is None:
            return []

        result: List[str] = []

        def dfs(current: TrieNode, path: str) -> None:
            if current.is_end_of_word:
                result.append(prefix + path)
            for char, child in current.children.items():
                dfs(child, path + char)

        dfs(node, "")
        return result

    def delete(self, word: str) -> bool:
        """
        단어 삭제 (재귀적으로 필요 없는 노드 정리)
        실제로 노드를 지우는 것은 까다로움. 여기서는 간단 버전.
        """
        def _delete(node: TrieNode, word: str, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0  # 자식이 없으면 이 노드 삭제 가능

            char = word[depth]
            if char not in node.children:
                return False

            should_delete_child = _delete(node.children[char], word, depth + 1)

            if should_delete_child:
                del node.children[char]
                return not node.is_end_of_word and len(node.children) == 0

            return False

        _delete(self.root, word, 0)
        return True  # 성공 여부는 더 정교하게 체크 가능


if __name__ == "__main__":
    trie = Trie()
    words = ["apple", "app", "apricot", "banana", "bat", "bath", "cat"]
    for w in words:
        trie.insert(w)

    print("search 'app':", trie.search("app"))
    print("search 'apple':", trie.search("apple"))
    print("search 'appl':", trie.search("appl"))

    print("starts_with 'ap':", trie.starts_with("ap"))
    print("starts_with 'ba':", trie.starts_with("ba"))
    print("starts_with 'z':", trie.starts_with("z"))

    print("words with prefix 'ap':", trie.get_words_with_prefix("ap"))
    print("words with prefix 'b':", trie.get_words_with_prefix("b"))

    trie.delete("app")
    print("app 삭제 후 search 'app':", trie.search("app"))
    print("app 삭제 후 search 'apple':", trie.search("apple"))  # 여전히 True여야 함