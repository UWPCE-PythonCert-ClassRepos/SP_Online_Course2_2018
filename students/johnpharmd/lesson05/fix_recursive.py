#!/usr/bin/env python3

# fix_recursive.py
import sys


def my_fun(n):
    for i in range(1, 101):
        if n == 2 ** i:
            return True
    return False


if __name__ == '__main__':
    n = int(sys.argv[1])
    print(my_fun(n))
