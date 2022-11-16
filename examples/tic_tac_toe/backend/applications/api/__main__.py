import logging
from dataclasses import dataclass
from threading import Thread
from typing import List, Type

from applications.api.bus_error_handler import BusErrorHandler
from applications.api.cqrs_api_app import CQRSAPIApp
from domain.games.scoring.domain_module import ScoringDomainModule
from domain.games.scoring.events import TopThreeListUpdated
from domain.games.scoring.queries import GetTopThreePlayers
from domain.games.tic_tac_toe.commands import CreateGame, PlaceMark, JoinGame
from domain.games.tic_tac_toe.domain_module import TicTacToeDomainModule
from domain.games.tic_tac_toe.events import GameCreated, BoardUpdated, WaitingForPlayerPlay, GameErrorOccurred, \
    GameEnded, GameStarted, MarkPlaced, TurnTimeout
from domain.users.commands import CreateUser
from domain.users.domain_module import UserDomainModule
from domain.users.events import UserInvited
from domain.users.online.events import UserConnected, UsersOnlineUpdated
from domain.users.online.queries import GetUsersOnline
from domain.users.queries import GetUser
from mani.domain.cqrs.effects import Event, Command, Query
from mani.domain.model.application.domain_application import DomainApplication
from mani.domain.model.application.net_config import NetConfig
from mani.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


def spawn(func, *args) -> None:
    thread = Thread(target=func, args=args, daemon=True)
    thread.start()


@dataclass(frozen=True)
class TicTacToeConfig(NetConfig):
    pass


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    logger.info(f"API starting...")
    domains = [TicTacToeDomainModule, UserDomainModule, ScoringDomainModule]
    events_to_publish: List[Type[Event]] = [GameCreated,
                                            GameStarted,
                                            BoardUpdated,
                                            WaitingForPlayerPlay,
                                            GameErrorOccurred,
                                            MarkPlaced,
                                            GameEnded,
                                            TopThreeListUpdated,
                                            UsersOnlineUpdated,
                                            UserInvited,
                                            TurnTimeout]
    accepted_events: List[Type[Event]] = [UserConnected, UserInvited]
    accepted_commands: List[Type[Command]] = [CreateGame, PlaceMark, CreateUser, JoinGame]
    accepted_queries: List[Type[Query]] = [GetTopThreePlayers, GetUsersOnline, GetUser]

    config = TicTacToeConfig(host="127.0.0.1", port=8080)

    domain = DomainApplication(domains=domains, config=config.__dict__)
    api_app = CQRSAPIApp(domain, config, accepted_commands, events_to_publish,
                         accepted_events=accepted_events,
                         accepted_queries=accepted_queries,
                         bus_error_effect_handler=BusErrorHandler)
    logger.info(f"API listening on: {config.host}:{config.port}")

    api_app.start()


if __name__ == "__main__":
    main()
