from abc import ABC, abstractmethod
from typing import Type, Callable

from mani.domain.cqrs.effects import Command


class CommandBus(ABC):
    @abstractmethod
    def handle(self, command: Command) -> None:
        pass

    @abstractmethod
    def subscribe(self, effect_type: Type[Command], handler: Callable[[Command], None]) -> None:
        pass
