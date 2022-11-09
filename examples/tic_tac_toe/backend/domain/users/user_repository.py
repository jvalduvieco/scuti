from abc import ABC

from domain.games.types import UserId
from mani.domain.model.repository.repository import Repository
from domain.users.user import User


class UserRepository(Repository[User, UserId], ABC):
    pass


ById = lambda e, r: r.by_id(e.id)
