#!/usr/bin/env python3

"""
Lesson3 - Recursion
"""


def factorial(n):
    if n <= 0:
        return
    elif n == 1:
        return 1
    else:
        return n * factorial(n - 1)
