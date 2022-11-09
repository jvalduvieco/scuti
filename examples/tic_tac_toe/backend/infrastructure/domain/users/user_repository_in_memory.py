from domain.games.types import UserId
from domain.users.user import User
from domain.users.user_repository import UserRepository
from mani.infrastructure.domain.model.repository.in_memory_repository import InMemoryRepository


class UserRepositoryInMemory(InMemoryRepository[User, UserId], UserRepository):
    pass
