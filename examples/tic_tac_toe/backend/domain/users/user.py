from dataclasses import dataclass
from datetime import datetime

from domain.games.types import UserId


@dataclass(frozen=True)
class User:
    id: UserId
    alias: str
    created_at: datetime
