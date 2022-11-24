from dataclasses import dataclass

from scuti.domain.cqrs.effects import FrameworkCommand
from scuti.domain.model.identifiable.identifier import Identifier


@dataclass(frozen=True)
class DeleteState(FrameworkCommand):
    id: Identifier
