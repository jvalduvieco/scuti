from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar


class Identifier(ABC):
    @abstractmethod
    def serialize(self):
        pass


IdentifierType = TypeVar("IdentifierType", bound=Identifier)
