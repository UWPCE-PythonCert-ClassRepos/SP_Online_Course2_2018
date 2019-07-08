"""
Name: Jared Mulholland
Assignment: Lesson_10 - memoization and profiling

fibonacci: 1, 1, 2, 3, 5, 8 ....

"""
from functools import lru_cache
import time
from timeit import timeit as timer

def fib(n):
    """function returns nth value in fibonacci sequence"""

    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n > 2:
        return fib(n-1) + fib(n-2)

start = time.time()

fib(35)

print("Without memoization getting the 35th value of the fibonacci sequence takes {:.0f} seconds".format(time.time() - start))

#### memoization #####

@lru_cache(maxsize = 1000)
def fib_memo(n):
    """function returns nth value in fibonacci sequence"""

    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n > 2:
        return fib_memo(n-1) + fib_memo(n-2)

start = time.time()

fib_memo(35)

print("With memoization getting the 35th value of the fibonacci sequence takes {:.0f} seconds".format(time.time() - start))

#Profiling

from timeit import timeit as timer

n_list = list(range(1,11))

repititions = 10000

print("\n\n Time to get first 10 fib seq using function with mapping")
print(timer(
    'map_fib = map(fib, n_list)',
    globals = globals(),
    number = repititions
))

print("\n\n Time to get first 10 fib seq using function with comprehension")
print(timer(
    'comprehension_fib = [fib(x) for x in n_list]',
    globals = globals(),
    number = repititions
))

print("\n\n Time to get first 10 fib seq using fib_memo function with mapping")
print(timer(
    'map_fib_memo = map(fib_memo, n_list)',
    globals = globals(),
    number = repititions
))

print("\n\n Time to get first 10 fib seq using fib_memo function with comprehension")
print(timer(
    'comprehension_fib_memo = [fib_memo(x) for x in n_list]',
    globals = globals(),
    number = repititions
))
