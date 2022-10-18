import abc
from typing import List, TypeVar, Callable, Type

from domain.cqrs.effects import Event
from domain.cqrs.bus.bus import Bus

T = TypeVar('T', bound=Event)


class EventBus(abc.ABC, Bus):
    @abc.abstractmethod
    def handle(self, events: List[Event]):
        pass

    @abc.abstractmethod
    def subscribe(self, event: Type[T], handler: Callable[[T], None]) -> None:
        pass
