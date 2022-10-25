import logging
from dataclasses import dataclass
from threading import Thread
from typing import List, Type

from applications.api.bus_error_handler import BusErrorHandler
from applications.api.cqrs_api_app import CQRSAPIApp
from domain.games.tic_tac_toe.commands import NewGame, PlaceMark
from domain.games.tic_tac_toe.domain_module import TicTacToeDomainModule
from domain.games.tic_tac_toe.events import GameStarted, BoardUpdated, WaitingForPlayerPlay, GameErrorOccurred, \
    GameEnded
from mani.domain.cqrs.effects import Event, Command
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
    domains = [TicTacToeDomainModule]
    events_to_publish: List[Type[Event]] = [GameStarted,
                                            BoardUpdated,
                                            WaitingForPlayerPlay,
                                            GameErrorOccurred,
                                            GameEnded]
    accepted_commands: List[Type[Command]] = [NewGame, PlaceMark]

    config = TicTacToeConfig(host="127.0.0.1", port=8080)

    domain = DomainApplication(domains=domains, config=config.__dict__)
    injector = domain.injector()
    api_app = CQRSAPIApp(domain, config, accepted_commands, events_to_publish, bus_error_effect_handler=BusErrorHandler)
    logger.info(f"API listening on: {config.host}:{config.port}")

    api_app.start()


if __name__ == "__main__":
    main()
