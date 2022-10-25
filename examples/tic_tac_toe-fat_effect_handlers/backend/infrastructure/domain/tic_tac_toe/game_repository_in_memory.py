from domain.games.tic_tac_toe.game import Game
from domain.games.tic_tac_toe.game_repository import GameRepository
from domain.games.types import GameId
from mani.infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository


class GameRepositoryInMemory(InMemoryRepository[Game, GameId], GameRepository):
    pass
