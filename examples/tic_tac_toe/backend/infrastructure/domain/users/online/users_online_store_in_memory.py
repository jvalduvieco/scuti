from domain.games.types import UserId
from domain.users.online.users_online_store import UsersOnlineStore

from scuti.infrastructure.domain.model.store.in_memory_store import InMemoryStore


class UsersOnlineStoreInMemory(UsersOnlineStore, InMemoryStore[UserId]):
    pass
