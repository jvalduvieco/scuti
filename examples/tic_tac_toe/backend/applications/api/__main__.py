"""
This is an example of using [Scuti](http://github.com/jvalduvieco/scuti/) to implement a multiplayer
distributed tic tac toe game.
Scuti is a set of libraries and the minimal code to implement a bus that delivers commands, events and queries to
handlers that change (for commands and queries) or retrieve (queries) the state of the system. It is a highly
customizable piece of code that, once customized, offers a clear view of the simple architecture showing a clear path
to the developer to implement features. The main pattern Scuti favors is CQS.

This example contains two parts:

 - **Backend**: Which takes care of the game logic and message passing across clients. (it's this code)
 - **Frontend**: Which controls user interface and sends and receives messages. Communication between backend and
 frontend is done using websockets for events and POST requests for commands and queries.

"""
import logging
from typing import List, Type

"""
All code related to application infrastructure is placed in the `applications` module. In this case an application 
called `api` is created.
"""
from applications.api.application_infrastructure_module import ApplicationInfrastructureModule
from applications.api.config import TicTacToeConfig

"""
`CQRSAPIApp` (see [[cqrs_api_app.py]]) is an opinionated way to expose the domain to the network. This is not 
included in Scuti as 
wiring to 
the outside world can be a complex thing that needs customization so it is outside Scuti scope.
It includes a:
 
 - [Flask](https://flask.palletsprojects.com/en/2.2.x/) application: Which takes care of three POST endpoints (
 `/commands`, `/queries`, `/events`)
 - [Flask socket.io](https://flask-socketio.readthedocs.io/en/latest/): A socket IO server embedded in flask that 
 takes care of Websockets.
 - Dependency [Injector](https://github.com/alecthomas/injector): That holds all dependencies and builds objects and 
 functions
 - A multi dispatch library [Plum] so handlers can have multiple `handle` methods.
"""
from applications.api.cqrs_api_app import CQRSAPIApp
from applications.api.websockets.commands import AssociateUserToSession
from applications.api.websockets.events import SessionDisconnected

"""
All domain logic is placed in the domain python module and split in subdomains according to the designed model.
"""
from domain.games.scoring.domain_module import ScoringDomainModule
from domain.games.scoring.events import TopThreeListUpdated
from domain.games.scoring.queries import GetTopThreePlayers
from domain.games.tic_tac_toe.commands import CreateGame, JoinGame, PlaceMark
from domain.games.tic_tac_toe.game_domain_module import TicTacToeDomainModule
from domain.games.tic_tac_toe.events import BoardUpdated, GameEnded, GameErrorOccurred, GameStarted, MarkPlaced, \
    TurnTimeout, WaitingForPlayerPlay
from domain.users.commands import CreateUser
from domain.users.users_domain_module import UserDomainModule
from domain.users.events import UserInvited
from domain.users.online.events import UserConnected, UsersOnlineUpdated
from domain.users.online.queries import GetUsersOnline
from domain.users.queries import GetUser

"""
And finally some helper code to manage effects(commands, queries) and a `DomainApplication` that models a set of 
subdomains that:
    - Can be started or stopped
    - Can define some dependency injection bindings
    - Can run some code in threads
    - Have a set of effect handlers that take case of changing the system and publishing state
"""
from scuti.domain.cqrs.effects import Command, Event, Query
from scuti.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


def main():
    """
    Your app starts here! Let's go.
    """

    """
    Boring logging stuff
    """
    logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)

    logger.info(f"API starting...")

    # ### Domain model configuration
    """
    Which sub domains should be loaded?
    `DomainModule`s define the shape of a subdomain. We'll get into this later but, as can be seen, in this case 
    there is something about Tic tac toe rules, something about users, something about scoring and some application 
    stuff.
    
    See: [[domain/games/tic_tac_toe/game_domain_module.py]]
    
    Another interesting example is users domain Module: [[domain/users/game_domain_module.py]]
    """
    domains = [TicTacToeDomainModule, UserDomainModule, ScoringDomainModule, ApplicationInfrastructureModule]

    # These are the events that will be published to the network using Websockets
    events_to_publish: List[Type[Event]] = [
        GameStarted,
        BoardUpdated,
        WaitingForPlayerPlay,
        GameErrorOccurred,
        MarkPlaced,
        GameEnded,
        TopThreeListUpdated,
        UsersOnlineUpdated,
        UserInvited,
        TurnTimeout
    ]

    # These are the events that can come from other contexts through network
    accepted_events: List[Type[Event]] = [UserConnected, UserInvited, SessionDisconnected]
    # The commands that this domain accepts
    accepted_commands: List[Type[Command]] = [AssociateUserToSession, CreateGame, PlaceMark, CreateUser, JoinGame]

    # The queries that this domain accepts
    accepted_queries: List[Type[Query]] = [GetTopThreePlayers, GetUsersOnline, GetUser]

    # Some application config. This could come from env vars or a nice Toml file.
    config = TicTacToeConfig(host="0.0.0.0", port=8080)

    """
    `CQRSAPIApp` is your app that glues all the libraries, Scuti and runs the processes. This is meant to be created by 
    the 
    user here you can find an example but feel free to create your own.
    """
    api_app = CQRSAPIApp(config=config,
                         domains=domains,
                         accepted_commands=accepted_commands,
                         events_to_publish=events_to_publish,
                         accepted_events=accepted_events,
                         accepted_queries=accepted_queries)

    # ### Start the application
    """
    Let's start playing! This function should be blocking
    """
    logger.info(f"API listening on: {config.host}:{config.port}")
    api_app.start()


if __name__ == "__main__":
    main()
