from abc import abstractmethod
from typing import Iterator

from domain.games.tic_tac_toe.game import Game
from domain.games.types import GameId
from mani.domain.model.repository.repository import Repository


class GameRepository(Repository[Game, GameId]):
    pass
