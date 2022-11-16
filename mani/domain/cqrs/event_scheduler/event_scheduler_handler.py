from injector import inject
from plum import dispatch

from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.event_scheduler.commands import ScheduleEvent, CancelScheduledEvents
from mani.domain.cqrs.event_scheduler.scheduled_events_store import ScheduledEventsStore
from mani.domain.time.monotonic_clock import MonotonicClock


class EventSchedulerHandler(EffectHandler):
    @inject
    def __init__(self, store: ScheduledEventsStore, clock: MonotonicClock):
        self.__clock = clock
        self.__store = store

    @dispatch
    def handle(self, effect: ScheduleEvent):
        if effect.update_every is not None and effect.update_event is not None:
            self.__schedule_updates(effect)
        self.__store.schedule(effect.when,
                              event=effect.event,
                              key=effect.key)
        return None, []

    @dispatch
    def handle(self, effect: CancelScheduledEvents):
        self.__store.remove(effect.key)
        return None, []

    def __schedule_updates(self, effect: ScheduleEvent):
        push_times = range(0, effect.when, effect.update_every)
        total = len(push_times)
        events = [(timeout, effect.update_event(order=index, total=total))
                  for index, timeout in enumerate(push_times, 1)]
        [self.__store.schedule(timeout, update, key=effect.key) for timeout, update in events]
