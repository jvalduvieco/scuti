from dataclasses import dataclass, field
from typing import Optional, Type, TypeVar

from examples.tic_tac_toe.backend.domain.operation_id import OperationId
from scuti.domain.cqrs.effects import Command, Event
from scuti.domain.cqrs.event_scheduler.events import UpdateEvent
from scuti.domain.time.units import Millisecond

T = TypeVar("T", bound=UpdateEvent)


@dataclass(frozen=True)
class ScheduleEvent(Command):
    event: Event
    when: Millisecond
    key: str
    operation_id: OperationId
    update_event: Optional[Type[T]] = field(default=None)
    update_every: Optional[int] = field(default=None)


@dataclass(frozen=True)
class CancelScheduledEvents(Command):
    operation_id: OperationId
    key: Optional[str] = field(default=None)
