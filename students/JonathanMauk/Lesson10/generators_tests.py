import math
import time


def intsum(a=0, b=0):
    """
    Sum of the integers:
        keep adding the next integer
        0 + 1 + 2 + 3 + 4 + 5 + …
        so the sequence is:
        0, 1, 3, 6, 10, 15 …..
    """
    while True:
        b += a
        yield b
        a += 1


def doubler(a=1):
    """
    Doubler:
        Each value is double the previous value:
        1, 2, 4, 8, 16, 32,
    """
    while True:
        yield a
        a *= 2


def fib(a=1, b=1):
    """
    The Fibonacci sequence as a generator:
        f(n) = f(n-1) + f(n-2)
        1, 1, 2, 3, 5, 8, 13, 21, 34…
    """
    while True:
        yield a
        a, b = b, a + b


def prime(a=2):
    """
    Generate the prime numbers (numbers only divisible by them self and 1):
        2, 3, 5, 7, 11, 13, 17, 19, 23…
    """
    while True:
        if not [b for b in range(2, a) if a % b == 0]:
            yield a
        a += 1

