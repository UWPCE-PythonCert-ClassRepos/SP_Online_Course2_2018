#!/usr/bin/env python3


def recursive_factorial(n):
    if n < 0:
        return -1
    elif n < 2:
        return 1
    else:
        return n * recursive_factorial(n-1)
