from typing import Optional

import marshmallow_dataclass
import socketio
from applications.api.tools import to_javascript
from domain.games.tic_tac_toe.events import BoardUpdated, GameEnded, GameStarted, MarkPlaced, WaitingForPlayerPlay
from domain.users.events import UserInvited
from domain.users.online.events import UserConnected
from injector import inject
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.effects import Event
from mani.infrastructure.logging.get_logger import get_logger
from mani.infrastructure.tools.string import camel_to_lower_snake
from plum import dispatch

logger = get_logger(__name__)


class EventToSocketIOBridge(EffectHandler):
    @inject
    def __init__(self, socketio_app: socketio.Server):
        self._socketio_app = socketio_app

    @dispatch
    def handle(self, event: Event) -> None:
        self.__emit(event, broadcast=True)

    @dispatch
    def handle(self, event: UserConnected) -> None:
        self.__emit(event, recipient=str(event.id))

    @dispatch
    def handle(self, event: UserInvited) -> None:
        self.__emit(event, recipient=str(event.invited))

    @dispatch
    def handle(self, event: BoardUpdated | WaitingForPlayerPlay | GameStarted | GameEnded | MarkPlaced):
        self.__emit(event, recipient=str(event.game_id))

    def __emit(self, event: Event, recipient: Optional[str] = None, broadcast: bool = False):
        schema = marshmallow_dataclass.class_schema(event.__class__)()
        converted_event = {"type": camel_to_lower_snake(event.__class__.__name__).upper(),
                           "payload": to_javascript(schema.dump(event))}
        self._socketio_app.emit(event="action", data=converted_event, to=recipient, broadcast=broadcast)
