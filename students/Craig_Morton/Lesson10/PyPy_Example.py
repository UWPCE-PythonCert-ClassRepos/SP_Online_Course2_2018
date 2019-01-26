# ------------------------------------------------- #
# Title: Lesson 10, PyPy vs Python generator speed test
# Dev:   Craig Morton
# Date:  1/19/2019
# Change Log: CraigM, 1/22/2019, PyPy vs Python generator speed test
# ------------------------------------------------- #

# Use PyPy as the runtime interpreter for code developed by students during the curriculum.

import time
from math import sqrt, factorial

times = 40


def fibonacci_recursive(n):
    """
    Fibonacci Sequence generator:
        f(n) = f(n-1) + f(n-2)
        1, 1, 2, 3, 5, 8, 13, 21, 34…
    """
    if n <= 1:
        return n
    else:
        return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)


def factorial_recursive(n):
    """
    Returns the factorial of a given non-negative integer,
    the product of all positive integers less than or equal to that number.
    """
    if n < 0:
        print(f"Please enter a non-negative integer. You entered {n}.")
        return
    elif n <= 1:
        return 1
    else:
        return n * factorial(n - 1)


if __name__ == "__main__":

    init = time.clock()
    for i in range(times):
        value = ((1+sqrt(5))**i-(1-sqrt(5))**i)/(2**i*sqrt(5))
    print(f"No function time for Fibonacci: {time.clock() - init}")

    init = time.clock()
    result = fibonacci_recursive(times)
    print(f"Function time for Fibonacci: {time.clock() - init}")

    init = time.clock()
    factorial(times)
    print(f"No function time for factorial: {time.clock() - init}")

    init = time.clock()
    result = factorial_recursive(times)
    print(f"Function time for factorial: {time.clock() - init}")


# Python interpreter results:
"""
No function time for Fibonacci: 6.649343280381473e-05
Function time for Fibonacci: 23.48703973730661
No function time for factorial: 3.3246716384383035e-06
Function time for factorial: 1.9393917902732483e-06
"""

# PyPy interpreter results:
"""
No function time for Fibonacci: 0.00010860594024623072
Function time for Fibonacci: 0.0939621469510406
No function time for factorial: 3.851077983221818e-05
Function time for factorial: 2.050214178117571e-05
"""
