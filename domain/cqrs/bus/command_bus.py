from abc import ABC, abstractmethod
from typing import Type, Callable

from domain.cqrs.effects import Command
from domain.cqrs.bus.bus import Bus


class CommandBus(ABC, Bus):
    @abstractmethod
    def handle(self, command: Command) -> None:
        pass

    @abstractmethod
    def subscribe(self, effect_type: Type[Command], handler: Callable[[Command], None]) -> None:
        pass
