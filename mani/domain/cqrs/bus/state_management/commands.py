from dataclasses import dataclass

from mani.domain.cqrs.effects import FrameworkCommand
from mani.domain.model.identifiable.identifier import Identifier


@dataclass(frozen=True)
class DeleteState(FrameworkCommand):
    id: Identifier
