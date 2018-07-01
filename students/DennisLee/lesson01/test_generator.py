#!/usr/bin/env python3

"""
test_generator.py

tests the solution to the generator lab

can be run with py.test or nosetests
"""

import generator_solution as gen


def test_intsum():

    g = gen.intsum()

    assert next(g) == 0
    assert next(g) == 1
    assert next(g) == 3
    assert next(g) == 6
    assert next(g) == 10
    assert next(g) == 15


def test_intsum2():

    g = gen.intsum2()

    assert next(g) == 0
    assert next(g) == 1
    assert next(g) == 3
    assert next(g) == 6
    assert next(g) == 10
    assert next(g) == 15


def test_doubler():

    g = gen.doubler()

    assert next(g) == 1
    assert next(g) == 2
    assert next(g) == 4
    assert next(g) == 8
    assert next(g) == 16
    assert next(g) == 32

    for i in range(10):
        j = next(g)

    assert j == 2**15


def test_fib():
    g = gen.fib()
    assert [next(g) for i in range(9)] == [1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_prime():
    g = gen.prime()
    for val in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        assert next(g) == val


##########################Dennis's work below###########################

def test_squared():
    g = gen.squared()
    for val in [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225]:
        assert next(g) == val

def test_cubed():
    g = gen.cubed()
    for val in [1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728, 2197]:
        assert next(g) == val

def test_threes():
    g = gen.threes()
    for val in [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45]:
        assert next(g) == val

def test_minus7():
    g = gen.minus7()
    for val in [0, -7, -14, -21, -28, -35, -42, -49, -56, -63, -70, -77, -84]:
        assert next(g) == val

def test_factorial():
    g = gen.factorial()
    for val in [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800, 39916800]:
        assert next(g) == val

def test_ten_to_xth_power():
    g = gen.ten_to_xth_power()
    for val in [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]:
        assert next(g) == val