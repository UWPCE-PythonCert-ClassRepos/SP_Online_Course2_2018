#!/usr/bin/env python3
__author__ = "Wieslaw Pucilowski"

def factorial(n):
    if n:
        return n * factorial(n -1)
    return 1

if __name__ == '__main__':
    print("Factorial for first 20 integers starting from 0")
    print("".join(['{}\n']*20).format(
        *[(x, factorial(x)) for x in range(20)]))