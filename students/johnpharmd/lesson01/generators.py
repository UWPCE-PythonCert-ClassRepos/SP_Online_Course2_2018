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


# def fib():
#     """
#     Fibonacci seq as a generator
#     """
#     n = 0
#     x = 1
#     while True:
#         yield x
#         n += 1
#         if n == 1:
#             x = 1
#         elif n == 2:
#             x = 2
#         else:
#             x = sum([fib() for i in range(n-1)])


def prime():
    """
    Generates sequence of prime numbers
    """
    i = 2
    while True:
        if i % 2 == 1 and i % 3 == 1 and i % 5 == 1:
            print('.', end=' ')
            yield i
        i += 1
