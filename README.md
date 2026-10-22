# Python 자료구조 연습 (대학 컴공 학부 수준)

컴퓨터공학 학부생이 **자료구조의 핵심 개념** 을 제대로 이해하고 손으로 직접 구현해볼 수 있도록 만든 저장소입니다.

| 분류 | 상태 | 스택 | 바로 보기 |
| --- | --- | --- | --- |
| 기초 · 자료구조 | 완료 | Python · pytest | — |

> **핵심 원칙**
> - **정론(正論) 우선**: 대학 강의 / 교과서에서 가르치는 표준적인 구현 방식을 따름니다.
> - **교육용 코드**: Pythonic한 한 줄짜리 트릭보다 **명확하고 읽기 쉬운 코드** 를 우선합니다. (조금 비효율적이어도 OK)
> - **직접 구현 연습**: 각 자료구조별로 구현 파일 + 교육용 파일을 제공합니다.
> - **시간/공간 복잡도 명시**: 모든 주요 연산에 Big-O를 주석/문서화로 명확히 표시.

## 📚 추천 학습 순서

### 1단계: 선형 자료구조 (Linear)
1. Dynamic Array (동적 배열) ← **가장 중요** (amortized analysis 이해)
2. Singly Linked List
3. Doubly Linked List
4. Stack
5. Queue (+ Circular Queue)

### 2단계: 해시 & 기본 트리
6. Hash Table (Separate Chaining → Open Addressing)
7. Binary Tree + Traversals (재귀 vs 반복)
8. Binary Search Tree (BST)

### 3단계: 균형 탐색 트리 & 우선순위 큐
9. AVL Tree (회전 이해가 핵심)
10. Heap (Min-Heap / Max-Heap) + HeapSort

### 4단계: 문자열 + 비선형
11. Trie (Prefix Tree)
12. Graph (인접 리스트/행렬) + BFS/DFS

### 5단계: 고급 알고리즘 + 자료구조
13. Union-Find (Disjoint Set Union) — 경로 압축 + Rank
14. Graph 고급: Dijkstra, Kruskal, Prim, Topological Sort
15. Segment Tree (기본 버전)

## 📋 포함된 자료구조 및 복잡도

| 자료구조              | 주요 연산                  | 평균/최악 시간복잡도      | 비고                     |
|-----------------------|---------------------------|---------------------------|--------------------------|
| Dynamic Array         | append, pop, access, insert | O(1)amortized / O(n)     | resizing 이해 필수       |
| Singly Linked List    | insert front/back, delete | O(1) or O(n)              | head/tail 관리           |
| Doubly Linked List    | insert/delete anywhere    | O(1) with pointer         | prev/next                |
| Stack                 | push, pop, peek           | O(1)                      | LIFO                     |
| Queue                 | enqueue, dequeue          | O(1)                      | FIFO, Circular 추천      |
| Hash Table            | insert, get, delete       | O(1) 평균 / O(n) 최악     | Load Factor, Collision   |
| BST                   | insert, search, delete    | O(log n) 평균 / O(n)      | 편향 문제 → AVL로        |
| AVL Tree              | insert, search, delete    | O(log n) 보장             | **회전** 이 핵심          |
| Min/Max Heap          | insert, extract-min       | O(log n)                  | Priority Queue의 기반    |
| Trie                  | insert, search, prefix    | O(L) L=문자열 길이        | 문자열 집합에 강력       |
| Graph (Adj List)      | addEdge, BFS, DFS         | O(V+E)                    | 방향/무방향, 가중치      |
| Union-Find (DSU)      | find, union               | 거의 O(1) (Ackermann)     | 경로압축 + Union by Rank |
| Segment Tree          | update, range query       | O(log n)                  | 구간 합/최소 등          |

## 📁 프로젝트 구조

```
.
├── README.md
├── linear/                  # 선형 자료구조
│   ├── dynamic_array.py
│   ├── singly_linked_list.py
│   ├── doubly_linked_list.py
│   ├── stack.py
│   └── queue.py
├── trees/                   # 트리 계열
│   ├── binary_tree.py
│   ├── binary_search_tree.py
│   ├── avl_tree.py
│   ├── heap.py
│   └── trie.py
├── hash_tables/
│   └── hash_table.py
├── graphs/
│   ├── graph.py
│   └── graph_algorithms.py
├── advanced/
│   ├── union_find.py
│   └── segment_tree.py
├── practice/                # 직접 구현해보는 연습 공간
│   └── practice_template.py
├── examples/
│   └── basic_usage.py
├── tests/                   # pytest 테스트
│   └── test_*.py
└── .gitignore
```

## 🚀 시작하기

```bash
# 1. 저장소 클론 또는 다운로드 후 이동
cd data-structures-python

# 2. (권장) 가상환경 생성
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # macOS/Linux

# 3. 테스트 실행 (pytest 필요)
pip install pytest
pytest tests/ -v
```

각 파일 상단에는 해당 자료구조의 **개념 설명, 핵심 연산, 복잡도** 가 주석으로 정리되어 있습니다.

## 💡 연습 팁 (매우 중요)

1. **먼저 직접 구현해보기**
   - `practice/` 폴더에 각자 구현을 작성해보세요.
   - `linear/queue.py` 등을 참고만 하고, 처음부터 끝까지 혼자 써보는 걸 강력 추천합니다.

2. **테스트로 검증하기**
   - 각 구현 파일은 `tests/` 에 대응하는 테스트가 있습니다.
   - `pytest tests/test_queue.py -s` 로 실행하며 디버깅하세요.

3. **시각화하며 이해하기**
   - Linked List, Tree, Graph는 종이에 직접 그려보는 게 최고입니다.
   - `examples/basic_usage.py`를 실행해보고 직접 수정하면서 실험하세요.

4. **Python 내장과 비교하기**
   - 실제 개발에서는 `list`, `collections.deque`, `dict`, `heapq`를 쓰는 게 맞습니다.
   - 여기서는 "왜" 그런 게 필요한지, 내부가 어떻게 동작하는지 배우는 게 목적입니다.

## 📖 참고하면 좋은 자료

- **교과서**: Introduction to Algorithms (CLRS), Data Structures and Algorithm Analysis in C (Weiss)
- **한국어**: "쉽게 배우는 자료구조 with 파이썬", "자료구조와 알고리즘" (윤성우 외)
- **시각화**: https://visualgo.net , https://www.cs.usfca.edu/~galles/visualization/

## 라이센스

교육용으로 자유롭게 사용하세요. 직접 구현해보는 과정 자체가 가장 큰 학습입니다.

행운을 빕니다! 💪
"구현해본 사람만이 진짜 이해한다."

---

**관련 저장소** · [data_structure](https://github.com/JimProKing/data_structure) · [Cording_Test](https://github.com/JimProKing/Cording_Test)

<sub>[JimProKing](https://github.com/JimProKing) · 이영찬 — 전체 저장소는 프로필의 프로젝트 지도에서 분야별로 볼 수 있습니다.</sub>
<!-- jpk-footer -->
