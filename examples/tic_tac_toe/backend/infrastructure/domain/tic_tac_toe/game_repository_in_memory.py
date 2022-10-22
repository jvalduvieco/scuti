from backend.domain.games.tic_tac_toe.game import Game
from backend.domain.games.types import GameId
from infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository


class GameRepositoryInMemory(InMemoryRepository[Game, GameId]):
    pass
