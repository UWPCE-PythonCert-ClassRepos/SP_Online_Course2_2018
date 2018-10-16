#!/usr/bin/env python3


# Sum of integers usning a for loop
def intsum():
    sum = 0
    for i in range(1, 999999):
        yield sum
        sum += i


# Sum of integers using a while loop
def intsum2():
    init_int = 1
    sum = 0
    while True:
        yield sum
        sum += init_int
        init_int += 1


# Doubles the value of the previous value
def doubler():
    val = 1
    while True:
        yield val
        val *= 2


# Fibonacci sequence generator
def fib():
    val_1 = 1
    val_2 = 1
    while True:
        yield val_1
        val_1, val_2 = val_2, val_1 + val_2


# Generates the prime sequence for the given range
def prime():
    for num in range(2, 9999):
        if all(num % i != 0 for i in range(2, num)):
            yield num
