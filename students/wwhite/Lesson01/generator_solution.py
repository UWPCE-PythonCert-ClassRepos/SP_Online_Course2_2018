#!/usr/bin/env python

import math


def intsum():
    """
    Sum of the integers:
    keep adding the next integer so the sequence is:
    0, 1, 3, 6, 10, 15 …
    """
    i = 0
    int_sum = 0
    while True:
        int_sum += i
        yield int_sum
        i += 1


def doubler():
    """
    Doubler:
    Each value is double the previous value:
    1, 2, 4, 8, 16, 32
    """
    i = 1
    while True:
        yield i
        i *= 2


def fib():
    """
    Fibonacci sequence:
    The Fibonacci sequence as a generator (f(n) = f(n-1) + f(n-2)):
    1, 1, 2, 3, 5, 8, 13, 21, 34…
    """
    i_first = 0
    i_second = 1
    while True:
        series_sum = i_second
        yield series_sum
        series_sum = i_first + i_second
        i_first = i_second
        i_second = series_sum


def prime():
    """
    Generate the prime numbers (numbers only divisible by them self and 1):
    2, 3, 5, 7, 11, 13, 17, 19, 23…
    """
    count = 2

    while True:
        is_prime = True

        for x in range(2, int(math.sqrt(count) + 1)):
            if count % x == 0:
                is_prime = False
                break

        if is_prime:
            yield count

        count += 1
