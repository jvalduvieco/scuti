from typing import List, Type, Tuple, Any

from injector import Binder, SingletonScope, Module, Scope

from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.hooks.logging_effects_bus_hook import LoggingEffectsBusHook
from mani.domain.cqrs.event_scheduler.event_scheduler_handler import EventSchedulerHandler
from mani.domain.cqrs.event_scheduler.scheduled_events_store import ScheduledEventsStore
from mani.domain.model.modules import DomainModule
from mani.domain.time.monotonic_clock import MonotonicClock
from mani.domain.time.wall_clock import WallClock
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus_runner import asynchronous_bus_runner
from mani.infrastructure.domain.cqrs.event_scheduler.scheduled_events_runner import event_scheduler_runner
from mani.infrastructure.domain.cqrs.event_scheduler.scheduled_events_store_in_memory import \
    ScheduledEventsStoreInMemory
from mani.infrastructure.domain.time.MonotonicClock.real_monotonic_clock import RealMonotonicClock
from mani.infrastructure.domain.time.WallClock.real_wall_clock import RealWallClock


class CQRSModule(Module):
    def configure(self, binder: Binder):
        from mani.domain.cqrs.bus.command_bus import CommandBus
        from mani.domain.cqrs.bus.event_bus import EventBus
        from mani.domain.cqrs.bus.query_bus import QueryBus
        from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus
        from mani.infrastructure.domain.cqrs.bus.command_bus_facade import CommandBusFacade
        from mani.infrastructure.domain.cqrs.bus.event_bus_facade import EventBusFacade
        from mani.infrastructure.domain.cqrs.bus.local_asynchronous_bus import LocalAsynchronousBus
        from mani.infrastructure.domain.cqrs.bus.local_synchronous_query_bus import LocalSynchronousQueryBus
        asynchronous_bus = LocalAsynchronousBus()
        asynchronous_bus.register_hook(LoggingEffectsBusHook())
        query_bus = LocalSynchronousQueryBus()
        binder.bind(AsynchronousBus, asynchronous_bus, scope=SingletonScope)
        binder.bind(QueryBus, query_bus, scope=SingletonScope)
        binder.bind(EventBus, EventBusFacade, scope=SingletonScope)
        binder.bind(CommandBus, CommandBusFacade, scope=SingletonScope)
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
            asynchronous_bus_runner,
            event_scheduler_runner
        ]
