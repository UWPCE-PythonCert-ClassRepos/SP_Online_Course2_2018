import math
import time


def fib(a=1, b=1):
    """
    The Fibonacci sequence as a generator:
        f(n) = f(n-1) + f(n-2)
        1, 1, 2, 3, 5, 8, 13, 21, 34…
    """
    while True:
        yield a
        a, b = b, a + b


def factorial(n):
    """
    Returns the factorial of a given non-negative integer,
    the product of all positive integers less than or equal to that number.
    """
    if n == float:
        print(f"Please enter an integer. You entered {n}.")
        return
    elif n < 0:
        print(f"Please enter a non-negative integer. You entered {n}.")
        return
    elif n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

