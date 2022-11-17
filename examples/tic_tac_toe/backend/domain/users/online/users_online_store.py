from abc import ABC

from domain.games.types import UserId

from mani.domain.model.store.store import Store


class UsersOnlineStore(Store[UserId], ABC):
    pass
