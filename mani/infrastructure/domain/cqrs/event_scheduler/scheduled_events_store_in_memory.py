from dataclasses import dataclass, field
from queue import PriorityQueue
from threading import Condition
from typing import Optional

from injector import inject
from mani.domain.cqrs.effects import Event
from mani.domain.cqrs.event_scheduler.scheduled_events_store import ScheduledEventsStore
from mani.domain.time.monotonic_clock import MonotonicClock
from mani.domain.time.units import Millisecond


@dataclass(order=True)
class PrioritizedItem:
    timestamp: int
    event: Event = field(compare=False)
    key: Optional[str] = field(compare=False, default=None)


class ScheduledEventsStoreInMemory(ScheduledEventsStore):
    @inject
    def __init__(self, clock: MonotonicClock):
        self.__clock = clock
        self.__scheduled_events: PriorityQueue = PriorityQueue()
        self.__should_be_awake = Condition()

    def schedule(self, after: Millisecond, event: Event, key: str = None):
        with self.__should_be_awake:
            self.__scheduled_events.put(
                PrioritizedItem(
                    timestamp=self.__clock.now(after),
                    event=event,
                    key=key),
                block=True,
                timeout=1)
            self.__should_be_awake.notify_all()

    def next(self) -> Event:
        return self.__scheduled_events.get(block=False).event

    def is_empty(self) -> bool:
        return self.__scheduled_events.empty()

    def expired(self, now: Millisecond) -> Optional[Event]:
        with self.__should_be_awake:
            if not self.is_empty():
                event = self.next() if self._peek().timestamp <= now else None
                if event is not None:
                    self.__scheduled_events.task_done()
                return event
            else:
                return None

    def remove(self, key: str):
        with self.__should_be_awake:
            survivors = list(filter(lambda scheduled_event: scheduled_event.key != key, self.__scheduled_events.queue))
            self.__scheduled_events.queue.clear()
            for item in survivors:
                self.__scheduled_events.put(item)
            self.__should_be_awake.notify_all()

    def wait_for_next_expiration(self):
        with self.__should_be_awake:
            next_scheduled = self._peek()
            now = self.__clock.now()
            if next_scheduled is not None and next_scheduled.timestamp < now:
                return
            elif next_scheduled is not None:
                self.__should_be_awake.wait(timeout=(next_scheduled.timestamp - now) / 1000)
            else:
                self.__should_be_awake.wait()

    def _peek(self) -> Optional[PrioritizedItem]:
        if not self.is_empty():
            return self.__scheduled_events.queue[0]
        else:
            return None

    def shutdown(self):
        with self.__should_be_awake:
            self.__should_be_awake.notify_all()
