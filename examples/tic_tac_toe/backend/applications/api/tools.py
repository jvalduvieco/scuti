from typing import List, Dict

from scuti.infrastructure.tools.dict import apply_to_keys
from scuti.infrastructure.tools.string import camel_to_lower_snake, snake_to_lower_camel


def to_message_response(message: str):
    return {'message': message}


def from_javascript(data: Dict | List) -> Dict | List:
    if isinstance(data, list):
        return list(map(lambda x: apply_to_keys(x, camel_to_lower_snake), data))
    else:
        return apply_to_keys(data, camel_to_lower_snake)


def to_javascript(dictionary: Dict) -> Dict:
    return apply_to_keys(dictionary, snake_to_lower_camel)
