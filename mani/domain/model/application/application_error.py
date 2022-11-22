from dataclasses import dataclass

from mani.domain.errors import ErrorEvent


@dataclass(frozen=True)
class ApplicationError(ErrorEvent):
    pass
