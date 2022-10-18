from typing import List, Type

from injector import Binder, SingletonScope, Module

from domain.model.modules import DomainModule


class CQRSModule(Module):
    def configure(self, binder: Binder):
        from domain.cqrs.bus.command_bus import CommandBus
        from domain.cqrs.bus.event_bus import EventBus
        from domain.cqrs.bus.query_bus import QueryBus
        from domain.cqrs.effects import Effect
        from infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus
        from infrastructure.domain.cqrs.bus.command_bus_facade import CommandBusFacade
        from infrastructure.domain.cqrs.bus.event_bus_facade import EventBusFacade
        from infrastructure.domain.cqrs.bus.local_asynchronous_bus import LocalAsynchronousBus
        from infrastructure.domain.cqrs.bus.local_synchronous_query_bus import LocalSynchronousQueryBus
        asynchronous_bus = LocalAsynchronousBus[Effect]()
        query_bus = LocalSynchronousQueryBus()
        binder.bind(QueryBus, query_bus, scope=SingletonScope)
        binder.bind(EventBus, EventBusFacade, scope=SingletonScope)
        binder.bind(CommandBus, CommandBusFacade, scope=SingletonScope)
        binder.bind(AsynchronousBus, asynchronous_bus, scope=SingletonScope)


class CQRSDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module]]:
        return [CQRSModule]
