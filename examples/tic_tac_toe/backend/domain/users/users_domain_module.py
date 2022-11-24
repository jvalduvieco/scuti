from typing import List, Type, Tuple

from domain.users.online.users_online_handler import UsersOnlineHandler
from domain.users.online.users_online_store import UsersOnlineStore
from domain.users.user_handler import UserHandler
from domain.users.user_repository import UserRepository
from infrastructure.domain.users.online.users_online_store_in_memory import UsersOnlineStoreInMemory
from infrastructure.domain.users.user_repository_in_memory import UserRepositoryInMemory
from injector import Module, Scope, SingletonScope

from scuti.domain.model.modules import DomainModule


class UserDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        return [
            (UserRepository, UserRepositoryInMemory, SingletonScope),
            (UsersOnlineStore, UsersOnlineStoreInMemory, SingletonScope)
        ]

    def effect_handlers(self):
        return [
            (UserHandler, UserRepository),
            # There are a few interesting things in `UsersOnlineHandler`. Click here [[users_online_handler_py]]
            (UsersOnlineHandler, UsersOnlineStore)
        ]
