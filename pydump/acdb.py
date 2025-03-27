import collections
import contextlib
import json
import os.path
import typing
import threading


class MemDriver:
    # MemDriver cares to store data on memory, this means that MemDriver is fast. Since there is no expiration
    # mechanism, be careful that it might eats up all your memory.

    def __init__(self) -> None:
        self.data = {}

    def get(self, k: str) -> bytearray:
        return self.data[k]

    def has(self, k: str) -> bool:
        return k in self.data

    def rmi(self, k: str) -> None:
        self.data.pop(k)

    def set(self, k: str, v: bytearray) -> None:
        self.data[k] = v


class DocDriver:
    # DocDriver use the OS's file system to manage data. In general, any high frequency operation is not recommended
    # unless you have an enough reason.

    def __init__(self, root: str) -> None:
        self.root = root
        if not os.path.exists(self.root):
            os.makedirs(self.root)

    def get(self, k: str) -> bytearray:
        with open(os.path.join(self.root, k), 'rb') as f:
            return f.read()

    def has(self, k: str) -> bool:
        return os.path.exists(os.path.join(self.root, k))

    def rmi(self, k: str) -> None:
        os.remove(os.path.join(self.root, k))

    def set(self, k: str, v: bytearray) -> None:
        with open(os.path.join(self.root, k), 'wb') as f:
            f.write(v)


class LruDriver:
    # LruDriver implemention. In computing, cache algorithms (also frequently called cache replacement algorithms or
    # cache replacement policies) are optimizing instructions, or algorithms, that a computer program or a
    # hardware-maintained structure can utilize in order to manage a cache of information stored on the computer.
    # Caching improves performance by keeping recent or often-used data items in a memory locations that are faster or
    # computationally cheaper to access than normal memory stores. When the cache is full, the algorithm must choose
    # which items to discard to make room for the new ones.

    def __init__(self, size: int) -> None:
        self.data = collections.OrderedDict()
        self.size = size

    def get(self, k: str) -> bytearray:
        self.data.move_to_end(k)
        return self.data[k]

    def has(self, k: str) -> bool:
        return k in self.data

    def rmi(self, k: str) -> None:
        self.data.pop(k)

    def set(self, k: str, v: bytearray) -> None:
        if len(self.data) >= self.size:
            self.data.popitem(False)
        self.data[k] = v


class MapDriver:
    # MapDriver is based on DocDriver and use LruDriver to provide caching at its interface layer. The size of
    # LruDriver is always 1024.

    def __init__(self, root: str) -> None:
        self.doc_driver = DocDriver(root)
        self.lru_driver = LruDriver(1024)

    def get(self, k: str) -> bytearray:
        with contextlib.suppress(KeyError):
            return self.lru_driver.get(k)
        v = self.doc_driver.get(k)
        self.lru_driver.set(k, v)
        return v

    def has(self, k: str) -> bool:
        return self.lru_driver.has(k) or self.doc_driver.has(k)

    def rmi(self, k: str) -> None:
        self.doc_driver.rmi(k)
        self.lru_driver.rmi(k)

    def set(self, k: str, v: bytearray) -> None:
        self.doc_driver.set(k, v)
        self.lru_driver.set(k, v)


class Emerge:
    # Emerge is a actuator of the given drive. Do not worry, Is's concurrency-safety.

    def __init__(self, driver: MemDriver | DocDriver | LruDriver | MapDriver) -> None:
        self.driver = driver
        self.lock = threading.Lock()

    def __delitem__(self, k: str) -> None:
        self.rmi(k)

    def __getitem__(self, k: str) -> typing.Any:
        return self.get(k)

    def __setitem__(self, k: str, v: typing.Any) -> None:
        self.set(k, v)

    def get(self, k: str) -> typing.Any:
        with self.lock:
            v = self.driver.get(k)
            return json.loads(v)

    def has(self, k: str) -> bool:
        with self.lock:
            self.driver.has(k)

    def rmi(self, k: str) -> None:
        with self.lock:
            self.driver.rmi(k)

    def set(self, k: str, v: typing.Any) -> None:
        with self.lock:
            v = json.dumps(v).encode()
            self.driver.set(k, v)
