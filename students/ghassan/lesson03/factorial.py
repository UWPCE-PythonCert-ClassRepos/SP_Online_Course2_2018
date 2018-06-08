#!/usr/bin/env python3


def factorial(x):
    # print(x)
    if x == 1:
        return 1
    else:
        return x * factorial(x-1)

if __name__ == '__main__':
    print(factorial(5))
