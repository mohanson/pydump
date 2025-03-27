import collections
import threading
import typing


class Lru:
    # Lru cache. It is safe for concurrent access.

    def __init__(self, size: int) -> None:
        assert size > 0
        self.data = collections.OrderedDict()
        self.lock = threading.Lock()
        self.size = size

    def get(self, k: typing.Any) -> typing.Any:
        # Get looks up a key's value from the cache.
        with self.lock:
            self.data.move_to_end(k)
            return self.data[k]

    def has(self, k: typing.Any) -> bool:
        # Has returns true if a key exists.
        with self.lock:
            return k in self.data

    def len(self) -> int:
        # Len returns the number of items in the cache.
        with self.lock:
            return len(self.data)

    def rmi(self, k: typing.Any) -> None:
        # Rmi removes the provided key from the cache.
        with self.lock:
            self.data.pop(k)

    def set(self, k: typing.Any, v: typing.Any) -> None:
        # Set adds a value to the cache.
        with self.lock:
            if len(self.data) >= self.size:
                self.data.popitem(False)
            self.data[k] = v
