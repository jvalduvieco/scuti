from abc import ABC
from collections.abc import Mapping
from typing import List, Type, Tuple, Callable

from injector import Module, Scope

from mani.domain.cqrs.effects import Command
from mani.domain.cqrs.bus.effect_handler import EffectHandler


class DomainModule(ABC):
    def __init__(self, config: Mapping):
        self._config = config

    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        return []

    def init_commands(self) -> List[Command]:
        return []

    def effect_handlers(self) -> List[Type[EffectHandler]]:
        return []

    def processes(self) -> List[Callable]:
        return []
