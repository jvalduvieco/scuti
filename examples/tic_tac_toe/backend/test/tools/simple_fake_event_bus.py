from typing import List, Type, Callable

from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.effects import Event


class SimpleFakeEventBus(EventBus):
    def __init__(self):
        self.emitted_events = []

    def handle(self, event: Event):
        self.emitted_events += [event]

    def subscribe(self, event: Type[Event], handler: Callable[[Event], None]) -> None:
        pass
