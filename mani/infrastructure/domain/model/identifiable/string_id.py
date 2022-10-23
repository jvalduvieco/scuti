from __future__ import annotations

import random
import string
from dataclasses import dataclass, field

from mani.domain.model.identifiable.identifier import Identifier


def _random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


@dataclass(frozen=True)
class StringId(Identifier):
    id: str = field(default_factory=_random_string)

    def serialize(self):
        return self.id
