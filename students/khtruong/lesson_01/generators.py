#!/usr/bin/env python


def integer_sum(i=0):
    cur = i
    while True:
        yield cur
        i += 1
        cur = cur + i


def doubler(i=1):
    while True:
        yield i
        i *= 2


def fib(i=1, j=1):
    while True:
        yield i
        i, j = j, i + j


def prime(i=2):
    while True:
        if not [x for x in range(2, i) if i % x == 0]:
            yield i
        i += 1
