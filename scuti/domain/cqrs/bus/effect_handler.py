from abc import ABC, abstractmethod
from typing import Any

from scuti.domain.cqrs.effects import Effect


class EffectHandler(ABC):
    @abstractmethod
    def handle(self, effect: Effect):
        pass


class ManagedStateEffectHandler(ABC):
    @abstractmethod
    def handle(self, state: Any, effect: Effect):
        pass
