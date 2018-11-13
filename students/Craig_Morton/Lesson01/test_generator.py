# ------------------------------------------------- #
# Title: Lesson 1, pt 4, Generator Testing Assignment
# Dev:   Craig Morton
# Date:  11/9/2018
# Change Log: CraigM, 11/9/2018, Generator Testing Assignment
# ------------------------------------------------- #

# !/usr/bin/env python3

import generator_solution as generator


def test_intsum():
    y = generator.intsum()
    assert next(y) == 0
    assert next(y) == 1
    assert next(y) == 3
    assert next(y) == 6
    assert next(y) == 10
    assert next(y) == 15


def test_doubler():
    y = generator.doubler()
    assert next(y) == 1
    assert next(y) == 2
    assert next(y) == 4
    assert next(y) == 8
    assert next(y) == 16
    assert next(y) == 32
    for i in range(10):
        v = next(y)
    assert v == 2 ** 15


def test_fib():
    y = generator.fib()
    assert [next(y) for i in range(9)] == [1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_prime():
    y = generator.prime()
    for value in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        assert next(y) == value


if __name__ == "__main__":
    test_intsum()
    test_doubler()
    test_fib()
    test_prime()
