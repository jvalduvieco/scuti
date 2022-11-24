import unittest
from dataclasses import dataclass

from scuti.domain.cqrs.effects import Event
from scuti.domain.time.units import Millisecond
from scuti.infrastructure.domain.cqrs.event_scheduler.scheduled_events_store_in_memory import \
    ScheduledEventsStoreInMemory
from scuti.infrastructure.time.MonotonicClock.fake_monotonic_clock import FakeMonotonicClock


@dataclass(frozen=True)
class _AnEvent(Event):
    a_property: int


class TestScheduledEventsStore(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = FakeMonotonicClock(Millisecond(0))
        self.scheduled_events = ScheduledEventsStoreInMemory(self.clock)

    def test_expired_on_emtpy_list_returns_none(self):
        self.assertIsNone(self.scheduled_events.expired(self.clock.now()))

    def test_expired_on_a_list_with_expired_items_returns_an_expired_item(self):
        an_event = _AnEvent(a_property=42)
        self.scheduled_events.schedule(after=Millisecond(10), event=an_event)
        self.assertEqual(an_event, self.scheduled_events.expired(self.clock.now(Millisecond(20))))

    def test_scheduled_events_can_be_removed_by_key(self):
        an_event = _AnEvent(a_property=42)
        another_event = _AnEvent(a_property=72)
        self.scheduled_events.schedule(after=Millisecond(10), event=an_event, key='an_event')
        self.scheduled_events.schedule(after=Millisecond(20), event=another_event, key='another_event')
        self.scheduled_events.remove('an_event')
        self.assertEqual(another_event, self.scheduled_events.expired(Millisecond(self.clock.now() + 60)))
        self.assertTrue(self.scheduled_events.is_empty())
