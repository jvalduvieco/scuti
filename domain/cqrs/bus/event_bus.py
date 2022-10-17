import abc
from typing import List, TypeVar, Callable, Dict, Type, Optional

from domain.cqrs.effects import Event

T = TypeVar('T', bound=Event)


class EventBus(abc.ABC):
    @abc.abstractmethod
    def publish(self, events: List[Event]):
        pass

    @abc.abstractmethod
    def subscribe(self, event: Type[T], handler: Callable[[T], None]) -> None:
        pass
