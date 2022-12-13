def intersection_over_union(list_1: list, list_2: list) -> float:
  intersection_count = 0

  for elements in set(list_1):
    if elements in list_2:
      intersection_count += 1

  iou = intersection_count / len(set(list_1 + list_2))

  return iou
