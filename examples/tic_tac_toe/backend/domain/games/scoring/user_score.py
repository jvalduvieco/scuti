from dataclasses import dataclass

from domain.games.types import UserId


@dataclass(frozen=True)
class UserScore:
    id: UserId
    score: int
