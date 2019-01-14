"""
Lesson 1: Generators
"""

def intsum():
    """
    keep adding the next integer
    0 + 1 + 2 + 3 + 4 + 5 + …
    so the sequence is:
    0, 1, 3, 6, 10, 15 …
    """
    num = 0
    i = 1
    while True:
        yield num
        num += i
        i += 1


def doubler():
    """
    Each value is double the previous value:
    1, 2, 4, 8, 16, 32,
    """
    num = 1
    while True:
        yield num
        num *= 2

def fib():
    """
    The Fibonacci sequence as a generator:
    f(n) = f(n-1) + f(n-2)
    1, 1, 2, 3, 5, 8, 13, 21, 34…
    """
    num = 1
    nminus1 = 1
    nminus2 = 0
    while True:
        yield num
        num = nminus1 + nminus2
        nminus2 = nminus1
        nminus1 = num


def is_prime(num):
    """
    return True if num is prime, False if it is not
    """
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


def prime():
    """
    Next prime generator
    """
    num = 2
    while True:
        while not is_prime(num):
            num += 1
        yield num
        num += 1
