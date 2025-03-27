import pydump.lru


def test_lru_append():
    c = pydump.lru.Lru(4)
    c.set(1, 1)
    c.set(2, 2)
    c.set(3, 3)
    c.set(4, 4)
    c.set(5, 5)
    assert c.get(1) == None
    assert c.get(5) == 5


def test_lru_change():
    c = pydump.lru.Lru(4)
    c.set(1, 1)
    c.set(2, 2)
    c.set(3, 3)
    c.set(4, 4)
    c.set(1, 5)
    assert c.get(1) == 5


def test_lru_delete():
    c = pydump.lru.Lru(4)
    c.set(1, 1)
    c.set(2, 2)
    c.set(3, 3)
    c.set(4, 4)
    c.rmi(2)
    assert c.get(2) == None
    assert c.len() == 3


def test_lru_size():
    c = pydump.lru.Lru(4)
    assert c.len() == 0
    c.set(1, 1)
    assert c.len() == 1
    c.set(2, 2)
    assert c.len() == 2
    c.set(3, 3)
    assert c.len() == 3
    c.set(4, 4)
    assert c.len() == 4
    c.set(5, 5)
    assert c.len() == 4
