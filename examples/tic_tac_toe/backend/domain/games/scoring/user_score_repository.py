from abc import ABC

from domain.games.scoring.user_score import UserScore
from domain.games.types import UserId

from scuti.domain.model.repository.repository import Repository


class UserScoreRepository(Repository[UserScore, UserId], ABC):
    pass
