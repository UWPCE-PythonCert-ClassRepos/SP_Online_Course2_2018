import pytest
import generator as g

def test_sum_generator():
    s = g.sum_generator()
    l = []
    for x in s:
        l.append(x)
        if x>20:
            break
    assert l == [0, 1, 3, 6, 10, 15, 21]

def test_double_generator():
    d = g.double_generator()
    l = []
    for x in d:
        l.append(x)
        if x>20:
            break
    assert l == [1, 2, 4, 8, 16, 32]

def test_fibonacci_generator():
    f = g.fibonacci_generator()
    l = []
    for x in f:
        l.append(x)
        if x>20:
            break
    assert l == [0, 1, 1, 2, 3, 5, 8, 13, 21]

def test_prime_generator():
    f = g.prime_generator()
    l = []
    for x in f:
        l.append(x)
        if x>20:
            break
    assert l == [2, 3, 5, 7, 11, 13, 17, 19, 23]