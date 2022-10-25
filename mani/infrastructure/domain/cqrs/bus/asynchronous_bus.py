from abc import ABC, abstractmethod
from typing import Type, Callable, List

from mani.domain.cqrs.effects import Effect


class AsynchronousBus(ABC):
    @abstractmethod
    def drain(self, should_block: bool):
        pass

    @abstractmethod
    def handles(self, item_type: Type[Effect]) -> bool:
        pass

    @abstractmethod
    def handle(self, item_type: Effect | List[Effect]):
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    def subscribe(self, item_type: Type[Effect], handler: Callable[[Effect], None]):
        pass
