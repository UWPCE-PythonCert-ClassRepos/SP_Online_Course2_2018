#!/usr/bin/env python
""" A series of simple generators """

def intsum():
    # Add series of integers
    current, total = 0, 0
    while True:
        yield(total)
        current += 1
        total += current


def doubler():
    # Each value is double the previous value
    total = 1
    while True:
        yield(total)
        total *= 2


def fib():
    # Generate Fibonacci sequence
    n1, n2 = 0, 1
    while True:
        n1, n2 = n2, n1 + n2 
        yield (n1)


def prime():
    # Generate series of prime numbers
    current = 2
    while True:
        for i in range(2, current+1):
            if current % i == 0 and i != current:
                current += 1
                break
            elif i < current:
                pass 
            else:
                yield (current)
                current += 1
