"""
Dynamic Array (동적 배열) - 교육용 구현

개념:
- 고정 크기 배열을 기반으로 하지만, 용량이 부족해지면 더 큰 배열로 복사(resize)한다.
- Python의 list가 내부적으로 이 방식을 사용한다.
- 핵심: Amortized Time Complexity 분석

주요 연산 복잡도:
- append (끝에 추가): O(1) amortized (가끔 O(n) resize 발생)
- pop (끝에서 제거): O(1) amortized
- insert / delete at index i: O(n) (shift 발생)
- access by index: O(1)
- search (값으로 찾기): O(n)

교육 포인트:
- capacity vs size (len) 구분
- resize 전략 (보통 2배, 때는 1.5배)
- 빈 배열에서의 append 동작
"""

from typing import Any, Optional, Iterator


class DynamicArray:
    """ 교육용 동적 배열 구현 (Python list를 모방)"""

    def __init__(self, capacity: int = 1):
        if capacity < 1:
            capacity = 1
        self._capacity: int = capacity
        self._size: int = 0
        self._data: list[Any] = [None] * capacity

    def __len__(self) -> int:
        """ 현재 요소 개수 반환 (O(1))"""
        return self._size

    def __getitem__(self, index: int) -> Any:
        """ 인덱스로 접근 (O(1))"""
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        return self._data[index]

    def __setitem__(self, index: int, value: Any) -> None:
        """ 인덱스로 값 설정 (O(1))"""
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        self._data[index] = value

    def __iter__(self) -> Iterator[Any]:
        """ 요소 순회 (O(n))"""
        for i in range(self._size):
            yield self._data[i]

    def __repr__(self) -> str:
        return f"DynamicArray({list(self)})"

    @property
    def capacity(self) -> int:
        """ 현재 내부 배열의 용량"""
        return self._capacity

    def _resize(self, new_capacity: int) -> None:
        """ 내부 배열 크기를 new_capacity로 별경 (O(n))"""
        if new_capacity < self._size:
            new_capacity = self._size
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value: Any) -> None:
        """
        끝에 요소 추가 (O(1) amortized)
        용량이 부족하면 2배로 확장
        """
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def pop(self) -> Any:
        """
        끝에서 요소 제거 후 반환 (O(1) amortized)
        """
        if self._size == 0:
            raise IndexError("pop from empty DynamicArray")
        self._size -= 1
        value = self._data[self._size]
        self._data[self._size] = None  # GC 도움

        # 용량이 너무 크면 축소 (선택적, 교육용으로 구현)
        if self._size > 0 and self._size <= self._capacity // 4:
            self._resize(self._capacity // 2)

        return value

    def insert(self, index: int, value: Any) -> None:
        """
        index 위치에 삽입 (O(n))
        index가 size와 같으면 append와 동일
        """
        if not 0 <= index <= self._size:
            raise IndexError("Index out of range")

        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        # 뒤에서부터 한 칸씩 shift
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def delete(self, index: int) -> Any:
        """
        index 위치의 요소 삭제 후 반환 (O(n))
        """
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")

        value = self._data[index]
        # 앞당기기
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1

        if self._size > 0 and self._size <= self._capacity // 4:
            self._resize(self._capacity // 2)
        return value

    def index(self, value: Any) -> int:
        """ 값으로 인덱스 찾기 (O(n)). 없으면 ValueError"""
        for i in range(self._size):
            if self._data[i] == value:
                return i
        raise ValueError(f"{value} is not in DynamicArray")

    def clear(self) -> None:
        """ 모든 요소 제거 (O(1) - capacity는 유지)"""
        self._size = 0
        self._data = [None] * self._capacity

    def to_list(self) -> list[Any]:
        """Python list로 변환 (디버깅/테스트용)"""
        return [self._data[i] for i in range(self._size)]


# 간단한 데모
if __name__ == "__main__":
    arr = DynamicArray()
    print("초기 capacity:", arr.capacity)

    for i in range(10):
        arr.append(i)
        print(f"append {i:2d} -> size={len(arr):2d}, capacity={arr.capacity:2d}")

    print("arr[3] =", arr[3])
    arr[3] = 999
    print("arr[3] 수정 후:", arr)

    print("pop():", arr.pop())
    print("최종:", arr)
    print("to_list():", arr.to_list())