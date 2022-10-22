from typing import List, Type, Callable

from domain.cqrs.bus.event_bus import EventBus, T
from domain.cqrs.effects import Event


class SimpleFakeEventBus(EventBus):
    def __init__(self):
        self.emitted_events = []

    def handle(self, events: List[Event]):
        self.emitted_events += events

    def subscribe(self, event: Type[T], handler: Callable[[T], None]) -> None:
        pass
