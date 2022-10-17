from abc import ABC, abstractmethod
from typing import Type, List, Callable

from domain.cqrs.effects import Command, Effect


class CommandBus(ABC):
    @abstractmethod
    def handle(self, command: Command) -> None:
        pass

    @abstractmethod
    def register(self, effect_type: Type[Command], handler: Callable[[Command], None]) -> None:
        pass
