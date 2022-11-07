from typing import List, Type, Tuple

from domain.users.user_handler import UserHandler
from domain.users.user_repository import UserRepository
from infrastructure.domain.users.user_repository_in_memory import UserRepositoryInMemory
from injector import Module, Scope, SingletonScope
from mani.domain.model.modules import DomainModule


class UserDomainModule(DomainModule):
    def bindings(self) -> List[Type[Module] | Tuple[Type, Type, Type[Scope]]]:
        return [(UserRepository, UserRepositoryInMemory, SingletonScope)]

    def effect_handlers(self):
        return [(UserHandler, UserRepository)]
