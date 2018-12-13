
from math import factorial



def intsum():
    n = -1
    sum = 0
    while True:
        n += 1
        sum = n+sum
        yield sum

def intsum2():
    n = -1
    sum = 0
    while True:
        n += 1
        sum = n+sum
        yield sum

def doubler():
    dub = 1
    while True:
        yield dub
        dub = 2*dub


def fib():
    n_1 = 1
    n_2 = 0
    while True:
        n = n_1+n_2
        yield n_1
        n_2 = n_1
        n_1 = n

def is_prime(n):
    if n<2: return False
    for x in range(2, n):
        if n % x == 0:
            return False
    else: return True

def prime():
    n = 1
    while True:
        n += 1
        if is_prime(n):
            yield n

def cube():
    n = 0
    while True:
        n += 1
        yield n**3

def sine_series(theta):
    k = 0
    while True:
        term = ((-1)**k*theta**(2*k+1))/factorial(2*k+1)
        k += 1
        yield term

