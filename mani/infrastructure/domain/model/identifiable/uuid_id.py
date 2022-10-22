from __future__ import annotations

import uuid
from uuid import UUID

from mani.domain.model.identifiable.identifier import Identifier


class UuidId(Identifier):
    def __init__(self, initial_value: UUID | str = None):
        if isinstance(initial_value, UUID):
            self.__id = initial_value
        elif isinstance(initial_value, str):
            self.__id = UUID(initial_value)
        elif initial_value is None:
            self.__id = uuid.uuid4()
        else:
            raise ValueError(f"Provided initial value ({initial_value}) can not be used as a v4 uuid.")

    @property
    def id(self) -> UUID:
        return self.__id

    def __eq__(self, other: UuidId) -> bool:
        if not isinstance(other, UuidId):
            return False
        return other.id == self.__id

    def __str__(self):
        return str(self.__id)

    def __hash__(self):
        return self.__id.__hash__()

    def __repr__(self):
        return str(self)

    def serialize(self):
        return str(self)
