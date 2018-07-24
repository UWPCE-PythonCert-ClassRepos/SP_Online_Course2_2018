#!/usr/bin/python

def intsum():
    val = 0
    sum = 0
    while (True):
        sum += val
        val += 1
        yield sum

def doubler():
    total = 1
    while True:
        yield total
        total *= 2

def fib():
    fibn = 1
    fibnm1 = 1
    while True:
        yield fibnm1
        fibnm2 = fibnm1
        fibnm1 = fibn
        fibn = fibnm1 + fibnm2

def _is_prime(n):
    for i in range (2, int(n/2)+1):
        if (n%i) == 0:
            return False
    return True

def prime():
    n = 2 
    while True:
        if _is_prime(n):
            yield n
        if n == 1 or n == 2:
          n += 1
        else:
          n += 2
