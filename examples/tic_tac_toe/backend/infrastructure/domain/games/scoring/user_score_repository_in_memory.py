from domain.games.scoring.user_score_repository import UserScoreRepository
from domain.games.types import UserId
from mani.infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository
from domain.games.scoring.user_score import UserScore


class UserScoreRepositoryInMemory(InMemoryRepository[UserScore, UserId], UserScoreRepository):
    pass
