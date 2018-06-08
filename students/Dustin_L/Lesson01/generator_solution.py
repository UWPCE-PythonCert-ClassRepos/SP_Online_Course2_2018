#!/usr/bin/env python3
"""Generator Exercise Module"""


def intsum(start=0):
    i = curr = start
    while True:
        yield curr
        i += 1
        curr += i


def doubler(start=1):
    while True:
        yield start
        start *= 2


def fib(i=1):
    prev = i - 1 if i > 0 else 0
    while True:
        yield i
        i, prev = i + prev, i


def prime(i=2):
    while True:
        if i < 2 or not [x for x in range(2, i) if i % x == 0]:
            yield i
        i += 1
