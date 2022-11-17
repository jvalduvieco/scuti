import threading
from dataclasses import dataclass, field
from queue import PriorityQueue
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
        self.__mutex = threading.Lock()

    def schedule(self, after: Millisecond, event: Event, key: str = None):
        with self.__mutex:
            self.__scheduled_events.put(
                PrioritizedItem(
                    timestamp=self.__clock.now(after),
                    event=event,
                    key=key),
                block=True,
                timeout=1)

    def next(self) -> Event:
        return self.__scheduled_events.get(timeout=1).event

    def is_empty(self) -> bool:
        return self.__scheduled_events.empty()

    def expired(self, now: Millisecond) -> Optional[Event]:
        with self.__mutex:
            if not self.is_empty():
                event = self.next() if self._peek().timestamp <= now else None
                if event is not None:
                    self.__scheduled_events.task_done()
                return event
            else:
                return None

    def remove(self, key: str):
        with self.__mutex:
            survivors = list(filter(lambda scheduled_event: scheduled_event.key != key, self.__scheduled_events.queue))
            self.__scheduled_events.queue.clear()
            for item in survivors:
                self.__scheduled_events.put(item)

    def _peek(self) -> Optional[PrioritizedItem]:
        if not self.is_empty():
            return self.__scheduled_events.queue[0]
        else:
            return None
