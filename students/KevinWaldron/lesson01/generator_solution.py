#!/usr/bin/env python3

import math

def intsum():
    """ sum of integers generator """
    result = 0;
    i = 1;
    while True:
        yield result
        result = i + result
        i += 1

def intsum2():
    """ also sum of integers generator (?) """
    result = 0;
    i = 1;
    while True:
        yield result
        result = i + result
        i += 1

def doubler():
    """ double previous value generator """
    result = 1;
    while True:
        yield result
        if result == 1:
            result = 2
        else:
            result = 2 * result

def fib():
    """ fibonacci generator """
    prev2 = 0
    prev1 = 1
    result = 1;
    while True:
        yield result
        result = prev2 + prev1
        prev2 = prev1
        prev1 = result

def prime():
    """ prime number generator """
    result = 2;
    while True:
        yield result
        result += 1
        while not is_prime(result):
            result += 1

def is_prime(val):
    """ Returns true if val is prime number, false otherwise """
    # reject all even numbers
    if val % 2 == 0:
        return False

    # check every odd number up to sqrt of val
    for x in range(3, int(math.sqrt(val)) + 1, 2):
        if val % x == 0:
            return False
    return True