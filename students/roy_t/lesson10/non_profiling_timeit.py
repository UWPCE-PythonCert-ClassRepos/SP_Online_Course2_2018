import time
from timeit import timeit

"""
Generate the fibonacci sequence in three different ways and determine which method works best.
Three different methods are timed using the timeit module.
"""


def memoize(f):
    memo = {}

    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper


@memoize
def fib_memo(n):
    if n <= 1:
        return n
    else:
        return fib_memo(n-1) + fib_memo(n-2)


def fib_recursive(n):
    if n <= 1:
        return n
    else:
        return fib_recursive(n-1) + fib_recursive(n-2)


if __name__ == '__main__':
    start = time.time()

    print('Fib(35) =', fib_memo(35))
    print("Time to process memoized version: " + str(time.time() - start))

    start = time.time()
    print('\nFib(35) =', fib_recursive(35))
    print("Time to process recursive version: " + str(time.time() - start))

    print('\nGenerating timeit information for memoized version:')
    print(timeit('fib_memo(35)',globals=globals(), number=1))

    print('\nGenerating timeit information for recursive version:')
    print(timeit('fib_recursive(35)',globals=globals(), number=1))
