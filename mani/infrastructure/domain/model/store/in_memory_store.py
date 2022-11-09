from typing import TypeVar

from mani.domain.model.store.store import Store

T = TypeVar("T")


class InMemoryStore(Store[T]):
    def __init__(self, initial_value: T = None):
        initial_value = initial_value if initial_value is not None else None
        self.__data = initial_value

    def save(self, data: T):
        self.__data = data

    def get(self) -> T:
        return self.__data
