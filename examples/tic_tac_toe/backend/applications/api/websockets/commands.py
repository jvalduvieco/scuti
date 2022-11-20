from dataclasses import dataclass

from domain.games.types import UserId
from mani.domain.cqrs.effects import Command


@dataclass(frozen=True)
class AssociateUserToSession(Command):
    user_id: UserId
    session_id: str
