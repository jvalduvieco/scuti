import unittest
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import List, Type, Callable, Optional, Tuple, Dict
from unittest import TestCase

from plum import dispatch

from domain.cqrs.bus.effect_handler import EffectHandler
from domain.cqrs.bus.event_bus import EventBus, T
from domain.cqrs.effects import Command, Event
from domain.model.identifiable.identifiable_entity import IdentifiableEntity
from infrastructure.domain.model.identifiable.uuid_id import UuidId
from infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository


class GameId(UuidId):
    pass


class PlayerId(UuidId):
    pass


class OperationId(UuidId):
    pass


@dataclass(frozen=True)
class NewGame(Command):
    operation_id: OperationId
    game_id: GameId
    player_1: PlayerId
    player_2: PlayerId


@dataclass(frozen=True)
class TicTacToeBoard:
    cells: Dict[Tuple[int, int], PlayerId] = field(default_factory=dict)

    def place(self, x: int, y: int, player_id: PlayerId):
        self.__assert_valid_position(x, y)
        if not self.is_free(x, y):
            raise ValueError(f"Cell {x},{y} already used")

        return replace(self, cells={**self.cells, (x, y): player_id})

    def is_free(self, x: int, y: int) -> bool:
        return self.cells.get((y, x), None) is None

    def __assert_valid_position(self, x, y):
        if x > 2:
            raise ValueError(f"Invalid value {x} for x")
        if y > 2:
            raise ValueError(f"Invalid value {y} for y")


@dataclass(frozen=True)
class Game(IdentifiableEntity):
    id: GameId
    player_1: PlayerId
    player_2: PlayerId
    board: TicTacToeBoard
    waiting_for_player: Optional[PlayerId] = field(default=None)


class GameRepositoryInMemory(InMemoryRepository[Game, GameId]):
    pass


@dataclass(frozen=True)
class GameStarted(Event):
    game_id: GameId
    player_1: PlayerId
    player_2: PlayerId
    board: TicTacToeBoard
    parent_operation_id: OperationId


@dataclass(frozen=True)
class WaitingForPlayerPlay(Event):
    game_id: GameId
    player_id: PlayerId


@dataclass(frozen=True)
class PlaceMark(Command):
    operation_id: OperationId
    game_id: GameId
    player_id: PlayerId
    x: int
    y: int


@dataclass(frozen=True)
class BoardUpdated(Event):
    game_id: GameId
    board: TicTacToeBoard


class TicTacToeGame(EffectHandler):
    def __init__(self, game_repository: GameRepositoryInMemory, event_bus: EventBus):
        self.__game_repository = game_repository
        self.__event_bus = event_bus

    @dispatch
    def handle(self, command: NewGame) -> None:
        current_game = Game(id=command.game_id, player_1=command.player_1, player_2=command.player_2,
                            board=TicTacToeBoard(), waiting_for_player=command.player_1)
        self.__game_repository.save(current_game)
        self.__event_bus.handle([
            GameStarted(game_id=current_game.id,
                        player_1=current_game.player_1,
                        player_2=current_game.player_2,
                        board=current_game.board,
                        parent_operation_id=command.operation_id),
            BoardUpdated(game_id=current_game.id, board=current_game.board),
            WaitingForPlayerPlay(game_id=current_game.id,
                                 player_id=current_game.player_1)
        ])

    @dispatch
    def handle(self, command: PlaceMark):
        game_state = self.__game_repository.by_id(command.game_id)
        if game_state.waiting_for_player != command.player_id:
            self.__event_bus.handle([GameErrorOccurred(reason=GameErrorReasons.PLAYER_CAN_NOT_PLAY,
                                                       player=command.player_id,
                                                       game_id=game_state.id,
                                                       parent_operation_id=command.operation_id)])

        elif not game_state.board.is_free(command.x, command.y):
            self.__event_bus.handle([GameErrorOccurred(reason=GameErrorReasons.POSITION_ALREADY_FILLED,
                                                       player=command.player_id,
                                                       game_id=game_state.id,
                                                       parent_operation_id=command.operation_id)])
        else:
            next_game_state = replace(game_state,
                                      waiting_for_player=game_state.player_1 if game_state.waiting_for_player == game_state.player_2 else game_state.player_2,
                                      board=game_state.board.place(x=command.x, y=command.y,
                                                                   player_id=command.player_id))
            self.__game_repository.save(next_game_state)
            self.__event_bus.handle([BoardUpdated(game_id=game_state.id, board=next_game_state.board)])


class SimpleFakeEventBus(EventBus):
    def __init__(self):
        self.emitted_events = []

    def handle(self, events: List[Event]):
        self.emitted_events += events

    def subscribe(self, event: Type[T], handler: Callable[[T], None]) -> None:
        pass


class GameErrorReasons(Enum):
    PLAYER_CAN_NOT_PLAY = "PLAYER_CAN_NOT_PLAY"
    POSITION_ALREADY_FILLED = "POSITION_ALREADY_FILLED"


@dataclass(frozen=True)
class GameErrorOccurred(Event):
    game_id: GameId
    player: PlayerId
    reason: GameErrorReasons
    parent_operation_id: OperationId


class TestTicTacToeGame(TestCase):
    def setUp(self) -> None:
        self.event_bus = SimpleFakeEventBus()
        self.game_repository = GameRepositoryInMemory()
        self.a_game = TicTacToeGame(event_bus=self.event_bus, game_repository=self.game_repository)
        self.game_id = GameId()
        self.player_1 = PlayerId()
        self.player_2 = PlayerId()
        self.operation_id = OperationId()
        self.another_operation_id = OperationId()

    def test_a_game_can_be_started(self):
        self.a_game.handle(NewGame(game_id=self.game_id, operation_id=self.operation_id, player_1=self.player_1,
                                   player_2=self.player_2))
        self.assertEqual([GameStarted(game_id=self.game_id,
                                      player_1=self.player_1,
                                      player_2=self.player_2,
                                      board=TicTacToeBoard(),
                                      parent_operation_id=self.operation_id),
                          BoardUpdated(game_id=self.game_id, board=TicTacToeBoard()),
                          WaitingForPlayerPlay(game_id=self.game_id, player_id=self.player_1)],
                         self.event_bus.emitted_events)

    def test_a_player_can_play_if_it_is_her_turn(self):
        self.a_game.handle(NewGame(game_id=self.game_id, operation_id=self.operation_id, player_1=self.player_1,
                                   player_2=self.player_2))
        self.a_game.handle(
            PlaceMark(game_id=self.game_id, operation_id=self.another_operation_id, player_id=self.player_1, x=0, y=0))
        self.assertEqual([GameStarted(game_id=self.game_id,
                                      player_1=self.player_1,
                                      player_2=self.player_2,
                                      board=TicTacToeBoard(),
                                      parent_operation_id=self.operation_id),
                          BoardUpdated(game_id=self.game_id, board=TicTacToeBoard()),
                          WaitingForPlayerPlay(game_id=self.game_id, player_id=self.player_1),
                          BoardUpdated(game_id=self.game_id, board=TicTacToeBoard(cells={(0, 0): self.player_1})),
                          ],
                         self.event_bus.emitted_events)

    def test_a_player_can_not_play_if_it_is_not_her_turn(self):
        self.a_game.handle(NewGame(game_id=self.game_id, operation_id=self.operation_id, player_1=self.player_1,
                                   player_2=self.player_2))
        self.a_game.handle(PlaceMark(game_id=self.game_id,
                                     operation_id=self.another_operation_id,
                                     player_id=self.player_2, x=0, y=0))
        self.assertTrue(GameErrorOccurred(reason=GameErrorReasons.PLAYER_CAN_NOT_PLAY,
                                          player=self.player_2,
                                          game_id=self.game_id,
                                          parent_operation_id=self.another_operation_id)
                        in self.event_bus.emitted_events)

    def test_a_player_can_not_play_to_an_already_filled_position(self):
        third_operation_id = OperationId()
        self.a_game.handle(NewGame(game_id=self.game_id, operation_id=self.operation_id,
                                   player_1=self.player_1,
                                   player_2=self.player_2))
        self.a_game.handle(PlaceMark(game_id=self.game_id,
                                     operation_id=self.another_operation_id,
                                     player_id=self.player_1, x=0, y=0))
        self.a_game.handle(PlaceMark(game_id=self.game_id,
                                     operation_id=third_operation_id,
                                     player_id=self.player_2, x=0, y=0))
        self.assertTrue(GameErrorOccurred(reason=GameErrorReasons.POSITION_ALREADY_FILLED,
                                          player=self.player_2,
                                          game_id=self.game_id,
                                          parent_operation_id=third_operation_id)
                        in self.event_bus.emitted_events)


if __name__ == '__main__':
    unittest.main()
