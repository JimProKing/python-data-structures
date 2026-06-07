from hash_tables.hash_table import HashTable, LinearProbingHashTable


def test_separate_chaining():
    ht = HashTable()
    ht["a"] = 1
    ht["b"] = 2
    ht["a"] = 99
    assert ht["a"] == 99
    assert ht.get("b") == 2
    assert ht.delete("a")
    assert "a" not in ht


def test_linear_probing():
    lp = LinearProbingHashTable()
    lp.put("x", 10)
    lp.put("y", 20)
    assert lp.get("x") == 10
    lp.delete("x")
    assert lp.get("x") is None