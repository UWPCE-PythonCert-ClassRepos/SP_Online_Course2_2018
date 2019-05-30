#!/usr/bin/env python3

"""
Use the memory_profiler module to determine memory usage difference between two functions.
"""

from memory_profiler import profile


@profile(stream=open('list_profiler.log', 'w+'))
def list_profiling(n):
    big_list = [i for i in range(n)]
    return big_list


if __name__ == '__main__':
    n = 1000000
    list_profiling(n)
