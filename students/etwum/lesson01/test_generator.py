"""
test_generator.py

tests the solution to the generator lab

can be run with py.test or nosetests
"""
import pytest
import generator as gen


def test_int_sum():

    g = gen.int_sum()

    assert next(g) == 0
    assert next(g) == 1
    assert next(g) == 3
    assert next(g) == 6
    assert next(g) == 10
    assert next(g) == 15
