from dataclasses import dataclass

from mani.domain.cqrs.effects import Event, Effect


@dataclass(frozen=True)
class BusHandlerFailed(Event):
    effect: Effect
    error: str
    stack_trace: str
