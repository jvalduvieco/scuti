from typing import Type, Dict, Any, TypeVar

import marshmallow_dataclass

T = TypeVar("T")


def from_untyped_dict(data_class: Type[T], data: Dict[str, Any]) -> T:
    schema = marshmallow_dataclass.class_schema(data_class)()
    return schema.load(data)
