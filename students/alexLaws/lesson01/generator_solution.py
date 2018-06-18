#!/usr/bin/env python


def intsum(n=999999999):
    addition = 0
    num = 0
    while num < n:
        num += 1
        yield addition
        addition += num


def intsum2():
    add = 0
    num = 1
    while True:
        yield add
        add += num
        num += 1


def doubler():
    value = 1
    while True:
        yield value
        value = value * 2


def fib():
    value = 1
    last = 0
    second = 0
    while True:
        yield value
        second = last
        last = value
        value = last + second


def prime():
    num = 2
    while True:
        divisors = 0
        for i in range(1, num + 1):
            if num % i == 0:
                divisors += 1
        if divisors == 2:
            yield num
        num += 1


def squared():
    num = 1
    while True:
        yield num ** 2
        num += 1


def minus_seven():
    num = 1000
    while True:
        yield num
        num -= 7
