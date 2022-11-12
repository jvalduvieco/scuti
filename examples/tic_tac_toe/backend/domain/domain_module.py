from typing import List, Type, Tuple

from domain.clock import Clock
from infrastructure.domain.real_clock import RealClock
from injector import Module, Scope, SingletonScope
from mani.domain.model.modules import DomainModule


class BaseDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        return [(Clock, RealClock, SingletonScope)]
