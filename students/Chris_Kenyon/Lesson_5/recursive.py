#!/usr/bin/env python3
"""Recursive module"""
import sys

def my_func(n):
    if n == 2:
        return True
    return my_func(n / 2)

if __name__ == '__main__':
    n = int(sys.argv[1])
    print(my_func(n))