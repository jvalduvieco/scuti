import threading
from time import sleep

from injector import inject

from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.bus.events import InfrastructureError
from mani.domain.cqrs.event_scheduler.scheduled_events_store import ScheduledEventsStore
from mani.domain.time.monotonic_clock import MonotonicClock
from mani.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


@inject
def event_scheduler_runner(scheduled_events: ScheduledEventsStore,
                           event_bus: EventBus,
                           clock: MonotonicClock):
    logger.info("Starting event scheduler...")
    self = threading.current_thread()
    while getattr(self, "should_be_running", True):
        try:
            now = clock.now()
            event = scheduled_events.expired(now)
            if event is None:
                sleep(0.01)
            else:
                event_bus.handle(event)
        except Exception as e:
            event_bus.handle(InfrastructureError.from_exception(e))
    logger.info("Stopping event scheduler...")
