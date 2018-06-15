#!/usr/bin/env python3

def intsum():
    """
    Generates a sum of integers
    """
    int = 0
    sum = 0
    while True:
        sum += int
        int += 1
        yield sum


def doubler():
    """
    Generates a sequence of integers where each value is double the value
    of the previous integer
    """
    x = 1
    while True:
        yield x
        x *= 2


def fib():
    """
    Generates a Fibonacci sequence starting from (0, 1)
    """
    x = 0
    y = 1
    while True:
        yield y
        x, y = y, x + y

def prime():
    """
    Generates a list of Prime numbers. Uses a list comprehension to divide each integer
    by all numbers except 1 and itself, and only includes the primes.
    """
    y = 2
    while True:
        if not [x for x in range(2, y) if y % x == 0]:
            yield y
        y+=1