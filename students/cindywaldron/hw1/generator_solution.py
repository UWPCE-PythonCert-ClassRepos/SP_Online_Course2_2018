#!/usr/bin/env python3

from math import sqrt

def intsum():
    sum = 0
    val = 0
    while True:
        yield sum
        val += 1
        sum += val


def intsum2():
    sum = 0
    val = 0
    while True:
        yield sum
        val += 1
        sum += val

def doubler():
    double_val = 1
    while True:
        yield double_val
        double_val = double_val*2

def fib_func(n):
    if n < 2:
        return n
    return fib_func(n-2) + fib_func(n-1)

def fib():
    x = 0
    value = 0
    while True:
        x += 1
        value = fib_func(x)
        yield value

def is_prime(n):
    for i in range(2, int(sqrt(n))+1):
        if not n % i:
            return False
    return True

def prime():
    num = 2
    while True:
        if is_prime(num):
            yield num
        num += 1



