import pytest

from lib.metrics import intersection_over_union


def test_intersection_over_union():
    result = round(
        intersection_over_union(
            ["a", "b", "b", "c", "d", "e"], ["a", "d", "f", "g", "g"]
        ),
        3,
    )
    exp_result = round(2 / 7, 3)

    assert result == exp_result


def test_intersection_over_union_two_empty_lists():
    result = intersection_over_union([], [])
    exp_result = 0

    assert result == exp_result


def test_intersection_over_union_one_empty_list():
    result = intersection_over_union([], ["a", "a", "b", "c"])
    exp_result = 0

    assert result == exp_result


def test_intersection_over_union_identical_lists():
    result = intersection_over_union(["a", "b", "c", "a"], ["c", "b", "a", "a"])
    exp_result = 1

    assert result == exp_result


def test_intersection_over_union_distinct_lists():
    result = intersection_over_union(["a", "b", "c", "d"], ["e", "f", "g", "z"])
    exp_result = 0

    assert result == exp_result


def test_intersection_over_union_distinct_None_1():
    result = intersection_over_union([None, None, None], [None, None])
    exp_result = 0

    assert result == exp_result


def test_intersection_over_union_distinct_None_2():
    result = round(
        intersection_over_union(["a", "b", None], [None, None, None, "a", "c"]), 3
    )
    exp_result = round(1 / 3, 3)

    assert result == exp_result


def test_intersection_over_union_distinct_None_3():
    result = intersection_over_union(["a", None], [None, None])
    exp_result = 0

    assert result == exp_result


def test_intersection_over_union_distinct_None_4():
    result = intersection_over_union(["a", "a", "b", "c", None], ["a", "b", "c", "c"])
    exp_result = 1

    assert result == exp_result
