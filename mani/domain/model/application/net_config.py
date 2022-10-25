from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class NetConfig(Protocol):
    host: str
    port: int
