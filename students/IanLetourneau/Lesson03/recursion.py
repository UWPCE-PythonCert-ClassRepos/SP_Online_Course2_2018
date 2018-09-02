#!/usr/bin/env python3
# Ian Letourneau
# 8/30/2018

def factorial(n):
    """A function to recursively run through a given integer
    and return the factorial total."""
    if n <1:
        return 1
    else:
        total = n*factorial(n-1)
        return total

total = factorial(5)
print(total)