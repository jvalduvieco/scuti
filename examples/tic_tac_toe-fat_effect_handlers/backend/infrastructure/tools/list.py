from typing import List


def all_equal_and_not_none(iterator: List) -> bool:
    values = set(iterator)
    return len(values) == 1 and values.pop() is not None
