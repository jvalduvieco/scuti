from abc import abstractmethod
from typing import Type, Dict

from mani.domain.cqrs.effects import Effect


class Bus:
    @abstractmethod
    def subscribe(self, item_type, handler):
        pass

    @abstractmethod
    def handle(self, items):
        pass

    @abstractmethod
    def handles(self, item_type: Type[Effect]):
        pass

    @abstractmethod
    def handled(self) -> Dict[str, Type[Effect]]:
        pass
