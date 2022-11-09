from abc import ABC

from domain.games.types import UserId
from mani.domain.model.repository.repository import Repository
from domain.games.scoring.user_score import UserScore


class UserScoreRepository(Repository[UserScore, UserId], ABC):
    pass
