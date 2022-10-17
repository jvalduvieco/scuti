from typing import TypeVar, List, Type, Callable

from injector import inject

from domain.cqrs.bus.event_bus import EventBus
from domain.cqrs.effects import Event
from infrastructure.domain.cqrs.bus.local_asynchronous_bus import LocalAsynchronousBus

T = TypeVar('T', bound=Event)


class EventBusFacade(EventBus):
    @inject
    def __init__(self, bus: LocalAsynchronousBus):
        self.__bus = bus

    def publish(self, events: List[Event]):
        self.__bus.handle(events)

    def subscribe(self, effect_type: Type[T], handler: Callable) -> None:
        self.__bus.register(effect_type, handler)
