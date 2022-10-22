from dataclasses import dataclass
from unittest import TestCase

from mani.domain.cqrs.bus.bus_handler_failed import BusHandlerFailed
from mani.domain.cqrs.effects import Event
from mani.infrastructure.domain.cqrs.bus.event_bus_facade import EventBusFacade
from mani.infrastructure.domain.cqrs.bus.local_asynchronous_bus import LocalAsynchronousBus


@dataclass(frozen=True)
class AnEvent(Event):
    pass


@dataclass(frozen=True)
class AnotherEvent(Event):
    pass


class TestEventBusFacade(TestCase):
    def test_can_subscribe_event_handlers(self):
        event_bus = EventBusFacade(LocalAsynchronousBus())
        self.assertIsNone(event_bus.subscribe(AnEvent, lambda x: None))

    def test_can_subscribe_several_handlers_for_an_event(self):
        event_bus = EventBusFacade(LocalAsynchronousBus())
        event_bus.subscribe(AnEvent, lambda x: None)
        self.assertIsNone(event_bus.subscribe(AnEvent, lambda x: None))

    def test_can_handle_events_in_subscription_order(self):
        async_bus = LocalAsynchronousBus()
        event_bus = EventBusFacade(async_bus)
        called_event_handlers = []
        event_bus.subscribe(AnEvent, lambda x: called_event_handlers.append(1))
        event_bus.subscribe(AnEvent, lambda x: called_event_handlers.append(2))
        event_bus.handle([AnEvent()])
        async_bus.drain()
        self.assertEqual([1, 2], called_event_handlers)

    def test_one_failing_event_handler_does_not_stop_the_others(self):
        async_bus = LocalAsynchronousBus()
        event_bus = EventBusFacade(async_bus)

        called_event_handlers = []
        failures_handled = []

        def failure_handler(item: BusHandlerFailed):
            failures_handled.append(item)

        event_bus.subscribe(AnEvent, lambda x: 1 / 0)
        event_bus.subscribe(AnEvent, lambda x: called_event_handlers.append(2))
        event_bus.subscribe(BusHandlerFailed, failure_handler)
        event_bus.handle([AnEvent()])
        async_bus.drain()
        self.assertEqual([2], called_event_handlers)
        self.assertEqual(1, len(failures_handled))

    def test_events_without_subscribers_are_ignored(self):
        async_bus = LocalAsynchronousBus()
        event_bus = EventBusFacade(async_bus)

        called_event_handlers = []
        event_bus.subscribe(AnEvent, lambda x: called_event_handlers.append(2))
        event_bus.handle([AnotherEvent()])
        async_bus.drain()
        self.assertEqual([], called_event_handlers)
