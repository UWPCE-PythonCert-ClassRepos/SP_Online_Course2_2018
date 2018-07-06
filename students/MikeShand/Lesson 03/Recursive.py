#!/usr/bin/env python3

def factorial(n):
    if n == 0 or n ==1:
        return 1
    else:
        return n * factorial(n-1)


if __name__ == '__main__':

    print(factorial(5))
    print(factorial(8))
    print(factorial(1))
    print(factorial(25))
