#!/usr/bin/env python3

def factorial(n):
    if n < 1:
        raise ValueError(f"Invalid factorial value {n}")
    elif n == 1:
        return 1
    else:
        return n * factorial(n-1)

if __name__ == '__main__':
    # test a few values
    assert(factorial(5) == 120)
    assert(factorial(3) == 6)
    assert(factorial(10) == 3628800)