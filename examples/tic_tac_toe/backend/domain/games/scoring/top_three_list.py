from dataclasses import dataclass, field, replace
from typing import List

from domain.games.scoring.user_score import UserScore
from domain.games.types import UserId


@dataclass(frozen=True)
class TopThreeList:
    top_three: List[UserScore] = field(default_factory=list)

    def should_be_on_the_list(self, score: int):
        if len(self.top_three) == 0:
            return True
        else:
            return self.top_three[-1].score < score

    def include(self, player_id: UserId, score: int):
        new_list = [*filter(lambda s: s.id != player_id, self.top_three), UserScore(player_id, score)]
        new_list.sort(key=lambda e: e.score)
        new_list.reverse()
        return replace(self, top_three=new_list[0:3])
