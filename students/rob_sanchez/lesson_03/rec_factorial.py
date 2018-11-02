#!/usr/bin/env python3


def factorial(n):
    if (n < 0):
        return "Cannot compute the factorial of negative numbers."

    return n * factorial(n-1) if n > 0 else 1
