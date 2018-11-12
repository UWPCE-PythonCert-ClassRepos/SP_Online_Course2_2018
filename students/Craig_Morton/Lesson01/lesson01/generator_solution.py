# ------------------------------------------------- #
# Title: Lesson 1, pt 3, Generator Assignment
# Dev:   Craig Morton
# Date:  11/7/2018
# Change Log: CraigM, 11/7/2018, Generator Assignment
# ------------------------------------------------- #

# !/usr/bin/env python3


def intsum():
    """Sum of integers"""
    current = 0
    sum = 0
    while True:
        sum += current
        yield sum
        current += 1


def doubler():
    """Doubles previous value exponentially"""
    current = 1
    while True:
        yield current
        current *= 2


def fib():
    """Fibonacci sequence"""
    yield 1
    yield 1
    cur = [1, 1]
    while True:
        the_sum = sum(cur)
        cur[0] = cur[1]
        cur[1] = the_sum
        yield the_sum


def prime():
    """Prime number sequence"""
    num = 2
    while True:
        if not [x for x in range(2, num) if num % x == 0]:
            yield num
        num += 1
