from abc import ABC

from domain.games.tic_tac_toe.game import GameInProgress, GameWaitingForPlayers
from domain.games.types import GameId

from mani.domain.model.repository.repository import Repository


class GameRepository(Repository[GameInProgress | GameWaitingForPlayers, GameId], ABC):
    pass


ByGameId = lambda e, r: r.by_id(e.game_id)
