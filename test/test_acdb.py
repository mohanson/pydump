import pydump.acdb


def test_acdb_emerge_lru_driver_append():
    c = pydump.acdb.Emerge(pydump.acdb.LruDriver(4))
    c.set(1, 1)
    c.set(2, 2)
    c.set(3, 3)
    c.set(4, 4)
    c.set(5, 5)
    assert not c.has(1)
    assert c.get(5) == 5


def test_acdb_emerge_lru_driver_change():
    c = pydump.acdb.Emerge(pydump.acdb.LruDriver(4))
    c.set(1, 1)
    c.set(2, 2)
    c.set(3, 3)
    c.set(4, 4)
    c.set(1, 5)
    assert c.get(1) == 5


def test_acdb_emerge_lru_driver_delete():
    c = pydump.acdb.Emerge(pydump.acdb.LruDriver(4))
    c.set(1, 1)
    c.set(2, 2)
    c.set(3, 3)
    c.set(4, 4)
    c.rmi(2)
    assert not c.has(2)
