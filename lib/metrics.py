from typing import List, Any


def intersection_over_union(list_1: List[Any], list_2: List[Any]) -> float:

    if None in list_1:
      list_1 = list(filter(None, list_1))

    if None in list_2:
      list_2 = list(filter(None, list_2))

    if len(list_1) == 0 or len(list_2) == 0:
        return 0

    return len(set(list_1) & set(list_2)) / len(set(list_1 + list_2))
