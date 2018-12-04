# ------------------------------------------------- #
# Title: Lesson 3, Recursion/Factorial Assignment
# Dev:   Craig Morton
# Date:  11/25/2018
# Change Log: CraigM, 11/25/2018, Recursion/Factorial Assignment
# ------------------------------------------------- #

#!/usr/bin/env python3


def factorial(n):
    """"Determines factorial of n recursively"""
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)


if __name__ == '__main__':

    print(factorial(3))
    print(factorial(6))
    print(factorial(12))
    print(factorial(24))
