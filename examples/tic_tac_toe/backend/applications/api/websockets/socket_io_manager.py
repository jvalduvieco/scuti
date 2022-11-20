import socketio
from applications.api.websockets.commands import AssociateUserToSession
from applications.api.websockets.events import SessionDisconnected
from applications.api.websockets.sessions.session_repository import SessionRepository
from applications.api.websockets.sessions.socket_io_session import SocketIOSession
from domain.games.tic_tac_toe.events import GameEnded, GameStateReadyToBeCleaned
from domain.operation_id import OperationId
from domain.users.events import PlayerJoinedAGame
from domain.users.online.events import UserDisconnected
from injector import inject
from mani.domain.cqrs.bus.command_bus import CommandBus
from mani.domain.cqrs.bus.effect_handler import EffectHandler
from mani.domain.cqrs.bus.event_bus import EventBus
from mani.domain.cqrs.event_scheduler.commands import ScheduleEvent
from mani.domain.time.units import Millisecond
from plum import dispatch


class SocketIOManager(EffectHandler):
    @inject
    def __init__(self, socketio_app: socketio.Server, sessions: SessionRepository, event_bus: EventBus,
                 command_bus: CommandBus):
        self._command_bus = command_bus
        self._event_bus = event_bus
        self._sessions = sessions
        self._socketio_app = socketio_app

    @dispatch
    def handle(self, event: PlayerJoinedAGame):
        session_id = self._sessions.by_user_id(event.player_id)
        self._socketio_app.enter_room(session_id, str(event.game_id))

    @dispatch
    def handle(self, command: AssociateUserToSession):
        self._sessions.save(SocketIOSession(sid=command.session_id, id=command.user_id))
        self._socketio_app.enter_room(command.session_id, str(command.user_id))

    @dispatch
    def handle(self, event: SessionDisconnected):
        user_id = self._sessions.by_session_id(event.session_id)
        self._sessions.remove(event.session_id)
        self._socketio_app.leave_room(event.session_id, str(user_id))
        self._socketio_app.close_room(str(user_id))
        self._event_bus.handle(UserDisconnected(id=user_id, operation_id=OperationId()))

    @dispatch
    def handle(self, event: GameEnded):
        self._command_bus.handle(ScheduleEvent(GameStateReadyToBeCleaned(game_id=event.game_id),
                                               when=Millisecond(10000), key=str(event.game_id),
                                               operation_id=OperationId()))

    @dispatch
    def handle(self, event: GameStateReadyToBeCleaned):
        self._socketio_app.close_room(str(event.game_id))