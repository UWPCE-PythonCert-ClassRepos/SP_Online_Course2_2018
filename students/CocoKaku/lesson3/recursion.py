#!/usr/bin/env python3

"""
Lesson 3 Assignment: Recursion
"""

def fact(n):
    """
    Factorial of n

    :param n:
    :return:
    """
    if n == 0:
        return 1
    return n * fact(n - 1)


if __name__ == "__main__":
    for i in range(0, 11):
        print(f"{i:2d}! = {fact(i):,}")
    print(fact(9))
    print(fact(10))