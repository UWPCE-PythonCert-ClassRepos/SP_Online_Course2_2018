#!/usr/bin/env python


def intsum():
    """
    Adds next integer y to integer value store x
    """
    x = 0
    y = 0
    while True:
        x += y
        y += 1
        yield x


def doubler():
    """
    Doubles the value of x
    """
    x = 1
    while True:
        yield x
        x *= 2


def fib():
    """
    Fibonacci seq as a generator
    """
    n = 1
    x = 1
    while True:
        yield n
        n += 1
        x = sum([i for i in range(n)])
