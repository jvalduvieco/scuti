from dataclasses import dataclass
from typing import TypeVar
from unittest import TestCase

from domain.cqrs.bus.bus_handler_failed import BusHandlerFailed
from domain.cqrs.effects import Event
from infrastructure.domain.cqrs.bus.local_asynchronous_bus import LocalAsynchronousBus


@dataclass(frozen=True)
class AnItem:
    id: int


@dataclass(frozen=True)
class AnotherItem(Event):
    id: int


T = TypeVar('T')


class TestAsynchronousBus(TestCase):
    def setUp(self) -> None:
        self.bus = LocalAsynchronousBus()

    def test_can_run_until_there_are_no_more_items_to_handle(self):
        self.assertIsNone(self.bus.drain())

    def test_handlers_for_a_bus_item_can_be_subscribed(self):
        def handler(item: AnotherItem):
            pass

        self.assertIsNone(self.bus.subscribe(AnotherItem, handler))

    def test_can_bus_items_can_be_pushed(self):
        self.assertIsNone(self.bus.handle(AnotherItem))

    def test_handlers_are_called_when_a_bus_item_is_pushed(self):
        handlers_called = []

        def handler(item: AnotherItem):
            handlers_called.append(item)

        self.bus.subscribe(AnotherItem, handler)
        self.bus.handle(AnotherItem(id=1))
        self.bus.drain()
        self.assertEqual([AnotherItem(id=1)], handlers_called)

    def test_items_are_removed_from_the_bus_once_processed(self):
        called_handlers = []

        def spying_handler(item: AnotherItem):
            called_handlers.append(item)

        self.bus.subscribe(AnotherItem, spying_handler)
        self.bus.handle(AnotherItem(id=1))
        self.bus.drain()
        self.bus.drain()
        self.assertEqual([AnotherItem(id=1)], called_handlers)

    def test_can_check_if_an_item_type_has_a_handler(self):
        self.bus.subscribe(AnotherItem, lambda x: None)

        self.assertTrue(self.bus.handles(AnotherItem))
        IAmNotRegistered = bool
        self.assertFalse(self.bus.handles(IAmNotRegistered))

    def test_if_a_handler_fails_to_catch_an_exception_an_event_is_emitted(self):
        failures_handled = []

        def failing_handler(item: AnItem):
            i_will_fail = 1 / 0

        def failure_handler(item: BusHandlerFailed):
            failures_handled.append(item)

        self.bus.subscribe(BusHandlerFailed, failure_handler)
        self.bus.subscribe(AnItem, failing_handler)
        self.bus.handle(AnItem(id=1))
        self.bus.drain()

        self.assertEqual(BusHandlerFailed, type(failures_handled[0]))
