#!/usr/bin/env python3


from memory_profiler import profile

fp = open('memory_profiler.log', 'w+')


@profile(stream=fp)
def fib_profiling(n):
    if n <= 1:
        return n
    else:
        return fib_profiling(n-1) + fib_profiling(n-2)


if __name__ == '__main__':
    fib_profiling(10)
