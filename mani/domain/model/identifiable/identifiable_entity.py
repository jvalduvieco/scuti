from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from mani.domain.model.identifiable.identifier import IdentifierType


@dataclass(frozen=True)
class IdentifiableEntity(Generic[IdentifierType]):
    id: IdentifierType


IdentifiableEntityType = TypeVar("IdentifiableEntityType", bound=IdentifiableEntity)
