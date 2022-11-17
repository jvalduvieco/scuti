from abc import ABC

from domain.games.types import UserId
from domain.users.user import User

from mani.domain.model.repository.repository import Repository


class UserRepository(Repository[User, UserId], ABC):
    pass


ById = lambda e, r: r.by_id(e.id)
