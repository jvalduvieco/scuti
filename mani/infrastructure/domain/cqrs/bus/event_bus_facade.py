from typing import List, Type, Callable

from injector import inject

from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.effects import Event
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus


class EventBusFacade(EventBus):
    @inject
    def __init__(self, bus: AsynchronousBus):
        self.__bus = bus

    def handle(self, events: List[Event] | Event):
        self.__bus.handle(events)

    def subscribe(self, effect_type: Type[Event], handler: Callable[[Event], None]) -> None:
        self.__bus.subscribe(effect_type, handler)
