from dataclasses import dataclass

from scuti.domain.errors import ErrorEvent


@dataclass(frozen=True)
class ApplicationError(ErrorEvent):
    pass
