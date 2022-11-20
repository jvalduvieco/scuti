from abc import ABC, ABCMeta, abstractmethod


class SessionRepository(ABC):
    @abstractmethod
    def save(self, session):
        pass

    @abstractmethod
    def by_user_id(self, an_id):
        pass

    @abstractmethod
    def by_session_id(self, an_id):
        pass

    @abstractmethod
    def remove(self, an_id: str):
        pass
