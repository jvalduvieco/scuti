from typing import List, Type, Tuple

from injector import Module, Scope, inject, SingletonScope, Binder

from mani.infrastructure.domain.cqrs.effect_store.plain_effect_store import PlainEffectStore
from mani.domain.testing.save_effects_bus_hook import SaveEffectsBusHook
from mani.domain.cqrs.effect_store.effect_store import EffectStore
from mani.domain.cqrs.effects import Command
from mani.domain.model.modules import DomainModule
from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus


class TestingInjectorModule(Module):
    def configure(self, binder: Binder) -> None:
        injector = binder.injector
        injector.get(AsynchronousBus).register_hook(injector.get(SaveEffectsBusHook))


class TestingDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        return [
            (EffectStore, PlainEffectStore, SingletonScope),
            TestingInjectorModule
        ]

    @inject
    def init(self) -> List[Command]:
        return []
