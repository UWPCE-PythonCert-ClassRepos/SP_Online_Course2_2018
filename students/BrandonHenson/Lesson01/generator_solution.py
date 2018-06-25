# Brandon Henson
# Python 220
# Lesson 1
# 6-22-18
# Generators
# !/usr/bin/env python


def intsum(i=0, sum=0):
    while True:
        sum += i
        yield sum
        i += 1


def intsum_2(i=0, sum=0):
    while True:
        sum += i
        yield sum
        i += 1


def doubler(i=1):
    while True:
        yield i
        i *= 2


def fib(next=1, pre=0):
    while True:
        fib_n = next
        yield fib_n
        fib_n = pre + next
        pre = next
        next = fib_n


def prime(i=1):
    while True:
        if i != 1 and all([i % x for x in range(2, i)]):
            yield i
        i += 1
