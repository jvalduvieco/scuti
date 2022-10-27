from abc import ABC

from mani.domain.model.repository.repository import Repository

from domain.games.tic_tac_toe.game import Game
from domain.games.types import GameId


class GameRepository(Repository[Game, GameId], ABC):
    pass


ByGameId = lambda e, r: r.by_id(e.game_id)
