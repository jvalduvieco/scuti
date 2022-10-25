from typing import List, Type, Tuple, Any

from injector import Binder, SingletonScope, Module, Scope

from mani.domain.cqrs.effects import Effect, Query
from mani.domain.model.modules import DomainModule


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
        query_bus = LocalSynchronousQueryBus()
        binder.bind(AsynchronousBus, asynchronous_bus, scope=SingletonScope)
        binder.bind(QueryBus, query_bus, scope=SingletonScope)
        binder.bind(EventBus, EventBusFacade, scope=SingletonScope)
        binder.bind(CommandBus, CommandBusFacade, scope=SingletonScope)


class CQRSDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type[Any], Type[Any], Type[Scope]]]:
        return [CQRSModule]
