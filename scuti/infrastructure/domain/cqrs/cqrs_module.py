from typing import Any, List, Tuple, Type

from injector import Binder, Module, Scope, SingletonScope

from scuti.domain.cqrs.bus.effect_handler import EffectHandler
from scuti.domain.cqrs.bus.hooks.logging_effects_bus_hook import LoggingEffectsBusHook
from scuti.domain.cqrs.event_scheduler.event_scheduler_handler import EventSchedulerHandler
from scuti.domain.cqrs.event_scheduler.scheduled_events_store import ScheduledEventsStore
from scuti.domain.model.modules import DomainModule
from scuti.domain.time.monotonic_clock import MonotonicClock
from scuti.domain.time.wall_clock import WallClock
from scuti.infrastructure.domain.cqrs.bus.asynchronous_bus_runner import AsynchronousBusRunner
from scuti.infrastructure.domain.cqrs.event_scheduler.scheduled_events_runner import ScheduledEventsRunner
from scuti.infrastructure.domain.cqrs.event_scheduler.scheduled_events_store_in_memory import \
    ScheduledEventsStoreInMemory
from scuti.infrastructure.time.MonotonicClock.real_monotonic_clock import RealMonotonicClock
from scuti.infrastructure.time.WallClock.real_wall_clock import RealWallClock


class CQRSModule(Module):
    def configure(self, binder: Binder):
        from scuti.domain.cqrs.bus.command_bus import CommandBus
        from scuti.domain.cqrs.bus.event_bus import EventBus
        from scuti.domain.cqrs.bus.query_bus import QueryBus
        from scuti.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus
        from scuti.infrastructure.domain.cqrs.bus.command_bus_facade import CommandBusFacade
        from scuti.infrastructure.domain.cqrs.bus.event_bus_facade import EventBusFacade
        from scuti.infrastructure.domain.cqrs.bus.local_asynchronous_bus import LocalAsynchronousBus
        from scuti.infrastructure.domain.cqrs.bus.local_synchronous_query_bus import LocalSynchronousQueryBus
        asynchronous_bus = LocalAsynchronousBus()
        asynchronous_bus.register_hook(LoggingEffectsBusHook())
        binder.bind(AsynchronousBus, asynchronous_bus, scope=SingletonScope)
        binder.bind(EventBus, EventBusFacade, scope=SingletonScope)
        binder.bind(CommandBus, CommandBusFacade, scope=SingletonScope)
        query_bus = binder.injector.get(LocalSynchronousQueryBus)
        binder.bind(QueryBus, query_bus, scope=SingletonScope)
        binder.bind(MonotonicClock, RealMonotonicClock, scope=SingletonScope)
        binder.bind(WallClock, RealWallClock, scope=SingletonScope)
        binder.bind(ScheduledEventsStore, ScheduledEventsStoreInMemory, scope=SingletonScope)


class CQRSDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type[Any], Type[Any], Type[Scope]]]:
        return [CQRSModule]

    def effect_handlers(self) -> List[Type[EffectHandler]]:
        return [EventSchedulerHandler]

    def processes(self):
        return [
            AsynchronousBusRunner,
            ScheduledEventsRunner
        ]
