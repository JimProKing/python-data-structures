"""
Hash Table (해시 테이블)

구현 방식 2가지 (대학에서 가장 많이 다루는):
1. Separate Chaining (분리 연결법) ← 여기서 메인 구현
2. Open Addressing (개방 주소법) — Linear Probing, Quadratic Probing, Double Hashing

Separate Chaining:
- 각 버킷이 Linked List (또는 Python list) 를 가짐
- 충돌이 나면 해당 버킷의 리스트에 추가
- Load Factor = n / capacity 가 너무 커지면 resize

Open Addressing (간단 Linear Probing도 구현):

주요 연산:
- insert / get / delete : O(1) 평균, O(n) 최악 (모든 키가 같은 버킷)

교육 포인트:
- 좋은 해시 함수의 중요성
- Load Factor와 resize 타이밍
- Separate Chaining vs Open Addressing 장단점
- Python의 dict는 내부적으로 Open Addressing + 매우 정교한 해시 사용
"""

from typing import Any, Optional, List, Tuple


# ==================== Separate Chaining ====================

class HashTable:
    """
    Separate Chaining 방식 해시 테이블 (교육용)
    각 버킷은 (key, value) 쌍의 리스트를 가짐
    """

    def __init__(self, capacity: int = 8, load_factor_threshold: float = 0.75):
        self._capacity = capacity
        self._size = 0
        self._load_factor_threshold = load_factor_threshold
        # buckets: List of list of (key, value)
        self._buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(capacity)]

    def _hash(self, key: Any) -> int:
        """Python의 hash()를 사용하되 음수 방지"""
        return hash(key) % self._capacity

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: Any) -> bool:
        return self.get(key) is not None

    def __getitem__(self, key: Any) -> Any:
        val = self.get(key)
        if val is None:
            raise KeyError(key)
        return val

    def __setitem__(self, key: Any, value: Any) -> None:
        self.put(key, value)

    def __repr__(self) -> str:
        items = []
        for bucket in self._buckets:
            for k, v in bucket:
                items.append(f"{k!r}: {v!r}")
        return "{" + ", ".join(items) + "}"

    def _load_factor(self) -> float:
        return self._size / self._capacity

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0

        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v)  # 재해싱

    def put(self, key: Any, value: Any) -> None:
        """ 삽입 또는 갱신 O(1) 평균"""
        idx = self._hash(key)
        bucket = self._buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # 갱신
                return

        bucket.append((key, value))
        self._size += 1

        if self._load_factor() > self._load_factor_threshold:
            self._resize(self._capacity * 2)

    def get(self, key: Any) -> Optional[Any]:
        """ 검색 O(1) 평균"""
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key: Any) -> bool:
        """ 삭제 O(1) 평균"""
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                # 축소 (선택)
                if self._capacity > 8 and self._load_factor() < 0.25:
                    self._resize(self._capacity // 2)
                return True
        return False

    def items(self) -> List[Tuple[Any, Any]]:
        result = []
        for bucket in self._buckets:
            result.extend(bucket)
        return result

    def keys(self) -> List[Any]:
        return [k for k, v in self.items()]

    def values(self) -> List[Any]:
        return [v for k, v in self.items()]


# ==================== 간단한 Open Addressing (Linear Probing) ====================

class LinearProbingHashTable:
    """
    Open Addressing - Linear Probing 방식 (간단 버전)
    삭제 시 'DELETED' 마커를 사용해야 함 (search 시 건너뛰기 위함)
    """

    _DELETED = object()

    def __init__(self, capacity: int = 8):
        self._capacity = capacity
        self._size = 0
        self._keys: List[Any] = [None] * capacity
        self._values: List[Any] = [None] * capacity

    def _hash(self, key: Any) -> int:
        return hash(key) % self._capacity

    def __len__(self) -> int:
        return self._size

    def _probe(self, key: Any) -> int:
        """Linear probing으로 위치 찾기"""
        idx = self._hash(key)
        start = idx
        while True:
            if self._keys[idx] is None or self._keys[idx] is self._DELETED or self._keys[idx] == key:
                return idx
            idx = (idx + 1) % self._capacity
            if idx == start:
                raise OverflowError("Hash table is full")

    def put(self, key: Any, value: Any) -> None:
        if self._size >= self._capacity:
            self._resize(self._capacity * 2)

        idx = self._probe(key)
        if self._keys[idx] is None or self._keys[idx] is self._DELETED:
            self._size += 1
        self._keys[idx] = key
        self._values[idx] = value

    def get(self, key: Any) -> Optional[Any]:
        idx = self._hash(key)
        start = idx
        while self._keys[idx] is not None:
            if self._keys[idx] != self._DELETED and self._keys[idx] == key:
                return self._values[idx]
            idx = (idx + 1) % self._capacity
            if idx == start:
                break
        return None

    def delete(self, key: Any) -> bool:
        idx = self._hash(key)
        start = idx
        while self._keys[idx] is not None:
            if self._keys[idx] != self._DELETED and self._keys[idx] == key:
                self._keys[idx] = self._DELETED
                self._values[idx] = None
                self._size -= 1
                return True
            idx = (idx + 1) % self._capacity
            if idx == start:
                break
        return False

    def _resize(self, new_capacity: int) -> None:
        old_keys = self._keys
        old_values = self._values
        self._capacity = new_capacity
        self._keys = [None] * new_capacity
        self._values = [None] * new_capacity
        self._size = 0

        for k, v in zip(old_keys, old_values):
            if k is not None and k is not self._DELETED:
                self.put(k, v)


if __name__ == "__main__":
    print("=== Separate Chaining HashTable ===")
    ht = HashTable()
    ht["apple"] = 1
    ht["banana"] = 2
    ht["cat"] = 3
    ht["apple"] = 99  # overwrite
    print(ht)
    print("get banana:", ht.get("banana"))
    print("len:", len(ht))

    print("\n=== Linear Probing HashTable ===")
    lp = LinearProbingHashTable()
    lp.put("dog", 10)
    lp.put("cat", 20)
    lp.put("bird", 30)
    print("get cat:", lp.get("cat"))
    lp.delete("cat")
    print("after delete cat, get cat:", lp.get("cat"))