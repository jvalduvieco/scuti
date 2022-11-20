from applications.api.websockets.sessions.session_repository import SessionRepository
from applications.api.websockets.sessions.socket_io_session import SocketIOSession
from domain.games.types import UserId


class SessionRepositoryInMemory(SessionRepository):
    def __init__(self):
        self.__session_user = {}
        self.__user_session = {}

    def save(self, session: SocketIOSession):
        self.__user_session[session.id] = session.sid
        self.__session_user[session.sid] = session.id

    def by_user_id(self, an_id: UserId) -> str:
        return self.__user_session.get(an_id, None)

    def by_session_id(self, an_id: str) -> UserId:
        return self.__session_user.get(an_id, None)

    def remove(self, an_id: str):
        user_id = self.__session_user.get("an_id", None)
        if user_id is not None:
            del self.__session_user[an_id]
            del self.__user_session[user_id]
