#!/usr/bin/env python

def intsum(i=0):
    """
    An infinite generator that produces the sum of integers starting with i.
    For example: [0, 1, 3, 6, 10, 15]
    Each element is the sum of all integers between i and itself.
    """
    j = 0
    while True:
        yield i
        j += 1
        i += j

def doubler(i=1):
    """
    An infinite generator, starting with i, in which each value is double the
    previous value.
    """
    while True:
        yield i
        i *= 2

def fib():
    """
    An infinite fibonacci sequence generator.
    """
    i = 0
    while True:
        if i < 2:
            yield 1
            p1 = 1
            p2 = 1
        else:
            yield(p1+p2)
            temp = p2
            p2 = p1
            p1 = p1+temp
        i += 1


def prime(i = 2, stop=None):
    """
    An infinite prime number generator.
    """
    # While clever, this solution is O(N!) - very slow!
    while True:
        if i < 4:
            yield i
        else:
            pr = True
            # Call prime recursively to check if i is prime.
            for num in prime(2,i):
                # If i is not evenly divisible by any of the prime numbers
                # between (and including) 2 and itself, then it's prime
                if not i%num:
                    pr = False
                    break
            if pr:
                # If it's prime, yield it!
                yield i
        i += 1
        if stop is not None and i >= stop:
            break
