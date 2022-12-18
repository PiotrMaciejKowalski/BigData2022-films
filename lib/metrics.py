from typing import List, Any

def intersection_over_union(list_1: List[Any], list_2: List[Any]) -> float:

    if len(list_1) == 0 or len(list_2) == 0:
        return 0

    else:

        return len(set(list_1) & set(list_2)) / len(set(list_1 + list_2))
