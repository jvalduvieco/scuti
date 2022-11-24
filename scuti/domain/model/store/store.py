from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class Store(Generic[T], ABC):
    @abstractmethod
    def get(self) -> T:
        pass
