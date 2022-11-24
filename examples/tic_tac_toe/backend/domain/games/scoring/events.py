from dataclasses import dataclass

from domain.games.scoring.top_three_list import TopThreeList
from domain.games.types import UserId

from scuti.domain.cqrs.effects import Event


@dataclass(frozen=True)
class PlayerScoreChanged(Event):
    player_id: UserId
    score: int


@dataclass(frozen=True)
class TopThreeListUpdated(Event):
    previous: TopThreeList
    current: TopThreeList
