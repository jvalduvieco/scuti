from dataclasses import dataclass

from scuti.domain.cqrs.effects import Event


@dataclass(frozen=True)
class SessionDisconnected(Event):
    session_id: str
