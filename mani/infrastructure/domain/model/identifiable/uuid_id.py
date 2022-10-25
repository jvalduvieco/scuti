from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from mani.domain.model.identifiable.identifier import Identifier


@dataclass(frozen=True)
class UuidId(Identifier):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if not self.__is_uuidable(self.id):
            raise Exception(f'Non UUIDable value supplied to Uuuidable Id: {self.contents}')

    def __is_uuidable(self, possible_uuid: Any) -> bool:
        try:
            uuid.UUID(possible_uuid)
        except:
            return False
        return True

    def __eq__(self, other) -> bool:
        if not isinstance(other, UuidId):
            return False
        return other.id == self.id

    def __hash__(self):
        return self.id.__hash__()

    def serialize(self):
        return self.id
