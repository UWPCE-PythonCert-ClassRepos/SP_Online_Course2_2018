#!/usr/bin/env python3
# Ian Letourneau
# 7/6/2018


def sum_of_int(n):
    """A function create a generator that generates
    sequence of numbers in which each successive
    number is the index of the next number added to
    the previous total."""
    num = 0
    for i in range(n):
        num += i
        yield num


def doubler(n):
    """A function that creates a generator to
    generate double the previous value."""
    num = 1
    for i in range(n):
        yield num
        num = num*2


def fib(n):
    """A function that creates a generator to
    reproduce the fibonacci sequence."""
    count = 0
    num1 = 0
    num2 = 1
    while count < n:
        if count != 0:
            yield num1
        num1, num2 = num2, (num1+num2)
        count += 1


def prime(n):
    """A function that creates a generator to
    produce a sseries of only prime numbers."""
    num = 2
    while num < n:
        is_prime = True
        for x in range(2, num):
            if num % x == 0:
                is_prime = False
        if is_prime == True:
            yield num
        num += 1
