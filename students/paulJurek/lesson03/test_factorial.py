"""test suite for recursive factoial"""
from factorial_recursion import factorial
import pytest


@pytest.mark.parametrize("input, expected", [
    (1, 1),
    (2, 2),
    (3, 6),
    (5, 120)
])
def test_factorial_results(input, expected):
    assert factorial(input) == expected