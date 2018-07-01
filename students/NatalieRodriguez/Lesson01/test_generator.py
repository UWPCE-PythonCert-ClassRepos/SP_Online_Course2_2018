"""
test_generator.py

tests the solution to the generator lab

can be run with py.test or nosetests
"""

import generators as gen


def test_sum_ints():

    g = gen.sum_ints()

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


def test_fibonacci():
    g = gen.fibonacci()
    assert [next(g) for i in range(9)] == [1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_primes():
    g = gen.primes()
    for val in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
        assert next(g) == val


def test_squared():
    g = gen.squared()
    for val in [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400]:
        assert next(g) == val


def test_cubed():
    g = gen.cubed()
    for val in [1, 8, 27, 64, 125, 216, 343, 512, 729, 1000, 1331, 1728, 2197, 2744, 3375, 4096, 4913, 5832, 6859, 8000]:
        assert next(g) == val

