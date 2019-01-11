#!/usr/bin/env python3

__author__ = "roy_t - githubtater"

import math


def sum_of_integers():
    """Keep adding the next integer in the list"""
    sum_num, inc = 0, 1
    while True:
        yield sum_num
        sum_num += inc
        inc += 1


def doubler():
    """Each value is double the previous value."""
    val = 1
    while True:
        yield val
        val *= 2


def fibonacci_sequence():
    """Return the fibonacci series of length n."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def prime_numbers():
    """Generate the prime numbers."""
    count = 1
    while True:
        count += 1
        for i in range(2, int(math.sqrt(count) + 1)):
            if not count % i:
                break
        else:
            yield count


def squared_nums():
    """Square number generator"""
    num = 1
    while True:
        squared = num*num
        yield squared
        num += 1


def count_by_threes():
    """Count-by-three geneator"""
    x = 0
    while True:
        yield x
        x += 3


def cubed_nums():
    """cubed number generator"""
    num = 1
    while True:
        cubed = num**3
        yield cubed
        num += 1


def minus_7():
    """Subtract 7 from previous number generator"""
    x = 0
    while True:
        yield x
        x -= 7
