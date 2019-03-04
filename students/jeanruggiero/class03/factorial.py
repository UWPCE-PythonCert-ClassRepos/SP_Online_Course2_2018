#!/usr/bin/env python

def factorial(n):
    """Returns n!"""
    if not isinstance(n, int):
        raise TypeError('Factorial can only be computed for numbers ' + \
            'of type int.')
    if n < 2:
        # Base case
        return 1
    return n*factorial(n-1)

assert factorial(5) == 120
assert factorial(1) == 1
assert factorial(0) == 1
assert factorial(10) == 3628800
