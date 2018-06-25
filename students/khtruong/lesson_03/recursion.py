#!/usr/bin/env python


def factorial(n):
    if n > 1:
        return n * factorial(n-1)
    else:
        return n

if __name__ == "__main__":
    print(factorial(0))
    print(factorial(1))
    print(factorial(2))
    print(factorial(3))
    print(factorial(10))