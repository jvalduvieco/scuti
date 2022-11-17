import abc
from typing import Callable, Type

from mani.domain.cqrs.effects import Event


class EventBus(abc.ABC):
    @abc.abstractmethod
    def handle(self, events: Event):
        pass

    @abc.abstractmethod
    def subscribe(self, event: Type[Event], handler: Callable[[Event], None]) -> None:
        pass
