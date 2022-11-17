from domain.games.tic_tac_toe.game import GameWaitingForPlayers, GameInProgress
from domain.games.tic_tac_toe.game_repository import GameRepository
from domain.games.types import GameId

from mani.infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository


class GameRepositoryInMemory(InMemoryRepository[GameWaitingForPlayers | GameInProgress, GameId], GameRepository):
    pass
