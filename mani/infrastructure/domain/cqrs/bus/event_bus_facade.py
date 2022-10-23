from typing import TypeVar, List, Type, Callable, Dict

from injector import inject

from mani.domain.cqrs.bus.bus import Bus
from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.effects import Event, Effect

T = TypeVar('T', bound=Event)


class EventBusFacade(EventBus):
    @inject
    def __init__(self, bus: Bus):
        self.__bus = bus

    def handle(self, events: List[Event]):
        self.__bus.handle(events)

    def subscribe(self, effect_type: Type[T], handler: Callable) -> None:
        self.__bus.subscribe(effect_type, handler)

    def handled(self) -> Dict[str, Type[Effect]]:
        return self.__bus.handled()

    def handles(self, item_type: Type[Effect]):
        return self.__bus.handles(item_type)
