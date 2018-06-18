#!/usr/bin/env python3


from math import sqrt

def intsum():
    x, increment = 0, 1
    while True:
        yield x
        x += increment
        increment += 1

def intsum2():
    x = 0
    while True:
        yield x * (x + 1) / 2
        x += 1

def doubler():
    x = 1
    while True:
        yield x
        x *= 2

def fib():
    x, y = 0, 1
    while True:
        x, y = y, x + y
        yield x

def prime():
    x = 1
    while True:
        x += 1
        for i in range(int(sqrt(x)), 1, -1):
            if not x % i:
                break
        else:
            yield x

def squared():
    x = 1
    while True:
        yield x * x
        x += 1

def cubed():
    x = 1
    while True:
        yield x * x * x
        x += 1

def threes():
    x = 0
    while True:
        yield x
        x += 3

def minus7():
    x = 0
    while True:
        yield x
        x -= 7

def factorial():
    x, increment = 1, 1
    while True:
        x, increment = x * increment, increment + 1
        yield x

def ten_to_xth_power():
    x = 1
    while True:
        yield x
        x *= 10