from typing import List, Type, Tuple

from injector import Module, Scope, SingletonScope

from domain.games.tic_tac_toe.game_repository import GameRepository
from domain.games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame
from infrastructure.domain.tic_tac_toe.game_repository_in_memory import GameRepositoryInMemory
from mani.domain.model.modules import DomainModule


class TicTacToeDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        return [(GameRepository, GameRepositoryInMemory, SingletonScope)]

    def effect_handlers(self):
        return [(TicTacToeGame, GameRepository)]
