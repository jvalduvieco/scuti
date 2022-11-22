import threading
from time import sleep

import pyprctl
from injector import inject

from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.bus.events import InfrastructureError
from mani.domain.cqrs.event_scheduler.scheduled_events_store import ScheduledEventsStore
from mani.domain.time.monotonic_clock import MonotonicClock
from mani.infrastructure.logging.get_logger import get_logger
from mani.infrastructure.threading.thread import Thread

logger = get_logger(__name__)


class ScheduledEventsRunner(Thread):
    @inject
    def __init__(self, scheduled_events: ScheduledEventsStore, event_bus: EventBus, clock: MonotonicClock):
        super().__init__()
        self._clock = clock
        self._event_bus = event_bus
        self._scheduled_events = scheduled_events

    def get_name(self):
        return "Event scheduler"

    def execute(self):
        logger.info("Starting event scheduler...")
        while not self.should_stop():
            try:
                now = self._clock.now()
                event = self._scheduled_events.expired(now)
                if event is None:
                    sleep(0.01)
                else:
                    self._event_bus.handle(event)
            except Exception as e:
                self._event_bus.handle(InfrastructureError.from_exception(e))
        logger.info("Stopping event scheduler...")

    def wants_to_stop(self):
        pass
