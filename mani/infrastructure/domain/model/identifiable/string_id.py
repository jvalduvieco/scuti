from __future__ import annotations

import random
import string

from mani.domain.model.identifiable.identifier import Identifier


class StringId(Identifier):
    def __init__(self, initial_value: int | str = None):
        if initial_value is None:
            self.__id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        else:
            self.__id = str(initial_value)

    @property
    def id(self) -> str:
        return self.__id

    def __eq__(self, other: StringId) -> bool:
        if not isinstance(other, StringId):
            return False
        return other.id == self.__id

    def __str__(self):
        return self.__id

    def __hash__(self):
        return self.__id.__hash__()

    def __repr__(self):
        return str(self)

    def serialize(self):
        return str(self)
