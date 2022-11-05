import pytest

from lib.sample_class import sample_function

def test_sample_function():
    result = sample_function()
    exp_result = 1
    assert result == exp_result, 'function sample_function returns wrong output'