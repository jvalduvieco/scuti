from typing import Dict, Any, Callable, List, TypeVar

T = TypeVar("T")


def apply_to_keys(dictionary: Dict[T, Any], function: Callable[[T], T]) -> Dict[T, Any]:
    def apply_to_items(array: List, a_function: Callable[[T], T]) -> List:
        def convert_item(item):
            if isinstance(item, list):
                return apply_to_items(item, a_function)
            elif isinstance(item, dict):
                return apply_to_keys(item, a_function)
            else:
                return item

        return [convert_item(item) for item in array]

    new_dictionary = {}
    for k, v in dictionary.items():
        if isinstance(v, dict):
            new_dictionary[function(k)] = apply_to_keys(v, function)
        elif isinstance(v, list):
            new_dictionary[function(k)] = apply_to_items(v, function)
        else:
            new_dictionary[function(k)] = v

    return new_dictionary


def dict_remove_keys(a_dict: Dict[T, Any], a_key: List[T]) -> Dict[T, Any]:
    return {k: v for k, v in a_dict.items() if k not in a_key}
