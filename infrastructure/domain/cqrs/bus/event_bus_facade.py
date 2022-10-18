from typing import TypeVar, List, Type, Callable

from injector import inject

from domain.cqrs.bus.event_bus import EventBus
from domain.cqrs.effects import Event
from domain.cqrs.bus.bus import Bus

T = TypeVar('T', bound=Event)


class EventBusFacade(EventBus):
    @inject
    def __init__(self, bus: Bus):
        self.__bus = bus

    def handle(self, events: List[Event]):
        self.__bus.handle(events)

    def subscribe(self, effect_type: Type[T], handler: Callable) -> None:
        self.__bus.subscribe(effect_type, handler)
