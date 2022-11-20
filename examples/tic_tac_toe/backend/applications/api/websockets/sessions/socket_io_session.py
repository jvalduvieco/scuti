from dataclasses import dataclass

from domain.games.types import UserId


@dataclass(frozen=True)
class SocketIOSession:
    id: UserId
    sid: str
