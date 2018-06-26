#!/usr/bin/env python

"""
Lesson01 - Generators
"""


def intsum(i=0, sum=0):
    while True:
        sum += i
        i += 1
        yield sum


def doubler(i=1):
    while True:
        yield i
        i = i*2


def fib():
    while True:
        a, b = 1, 1
        while True:
            yield a
            a, b = b, a + b


def prime(n=2):
    while True:
        prime = True
        for i in range(2, n):
            if n % i == 0:
                prime = False
        if prime is True:
            yield n
        n += 1
