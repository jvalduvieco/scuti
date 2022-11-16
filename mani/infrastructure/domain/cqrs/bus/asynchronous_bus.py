from abc import ABC, abstractmethod
from typing import Type, Callable, List

from mani.domain.cqrs.bus.hooks.bus_hook import BusHook
from mani.domain.cqrs.effects import Effect


class AsynchronousBus(ABC):
    @abstractmethod
    def drain(self):
        pass

    @abstractmethod
    def handles(self, item_type: Type[Effect]) -> bool:
        pass

    @abstractmethod
    def handle(self, item_type: Effect):
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def subscribe(self, item_type: Type[Effect], handler: Callable[[Effect], None], human_friendly_name: str):
        pass

    @abstractmethod
    def register_hook(self, hook: BusHook):
        pass
