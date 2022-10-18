from typing import Iterable, Union, Callable, Any, List


def unique(a_list: Iterable,
           preserve_order: bool = True,
           unique_by: Union[None, Callable[[Any], Any]] = None) -> List:
    if not preserve_order and unique_by is None:
        return list(set(a_list))
    elif unique_by is None:
        # https://twitter.com/raymondh/status/944125570534621185
        # https://www.peterbe.com/plog/fastest-way-to-uniquify-a-list-in-python-3.6
        return list(dict.fromkeys(a_list))
    else:
        seen = set()
        seen_add = seen.add
        return [x for x in a_list if not (unique_by(x) in seen or seen_add(unique_by(x)))]
