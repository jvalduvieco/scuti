from dataclasses import dataclass

from domain.games.types import UserId
from mani.domain.cqrs.effects import Event


@dataclass(frozen=True)
class PlayerScoreChanged(Event):
    player_id: UserId
    score: int
