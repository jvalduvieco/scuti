from dataclasses import dataclass

from mani.domain.cqrs.effects import Event


@dataclass(frozen=True)
class SessionDisconnected(Event):
    session_id: str
