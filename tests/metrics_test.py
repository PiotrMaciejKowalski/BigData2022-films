import pytest

from lib.metrics import intersection_over_union

def test_intersection_over_union():
  result = round(intersection_over_union(["a","b","b","c","d","e"],["a","d","f","g","g"]),3)
  exp_result = round(2/7,3)

  assert result == exp_result
