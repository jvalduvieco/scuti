from typing import List, Type, Tuple

from domain.games.tic_tac_toe.game_repository import GameRepository
from domain.games.tic_tac_toe.tic_tac_toe_game import TicTacToeGame
from infrastructure.domain.games.tic_tac_toe.game_repository_in_memory import GameRepositoryInMemory
from injector import Module, Scope, SingletonScope

from scuti.domain.model.modules import DomainModule


class TicTacToeDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        """
        These are standard Injector bindings. It is possible to create Injector [modules](https://injector.readthedocs.io/en/latest/terminology.html#module
        """
        return [(GameRepository, GameRepositoryInMemory, SingletonScope)]

    def effect_handlers(self):
        """
        Effect handler definition require an effect handler type and a repository type.
        Repository will take care of EffectHandler states. Usually these states represent entities,
        sagas or projections.
        See  [[domain/games/tic_tac_toe/tic_tac_toe_game.py]] as example
        """
        return [(TicTacToeGame, GameRepository)]
