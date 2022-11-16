from dataclasses import dataclass
from typing import Protocol, Dict, runtime_checkable


# See https://stackoverflow.com/questions/54668000/type-hint-for-an-instance-of-a-non-specific-dataclass
@runtime_checkable
@dataclass
class Dataclass(Protocol):
    __dataclass_fields__: Dict
