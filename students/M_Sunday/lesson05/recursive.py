#!/usr/bin/env python3
import sys
import pdb


def my_fun(n):
    if n == 2:
        return True
    return my_fun(n/2)


if __name__ == '__main__':
    pdb.set_trace()
    n = int(sys.argv[1])
    print(my_fun(n))
