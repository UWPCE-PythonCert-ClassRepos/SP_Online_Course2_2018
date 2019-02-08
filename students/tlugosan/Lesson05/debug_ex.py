#!/usr/bin/env python3

import sys


def my_function(n):
    if n <= 1:
        return False
    if n == 2:
        return True

    return my_function(n/2)


if __name__ == "__main__":
    n = int(sys.argv[1])
    print(my_function(n))
