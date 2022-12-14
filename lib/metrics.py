from typing import List, Any

def intersection_over_union(list_1: List[Any], list_2: List[Any]) -> float:
  intersection_count = 0

  for elements in set(list_1):
    if  elements in list_2:
      intersection_count += 1

  return intersection_count / len(set(list_1 + list_2))
