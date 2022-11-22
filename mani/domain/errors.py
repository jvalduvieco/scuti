from abc import ABC
from dataclasses import dataclass
from types import TracebackType

from mani.domain.cqrs.effects import Event


@dataclass(frozen=True)
class ErrorEvent(Event, ABC):
    error: str
    stack_trace: TracebackType | None
