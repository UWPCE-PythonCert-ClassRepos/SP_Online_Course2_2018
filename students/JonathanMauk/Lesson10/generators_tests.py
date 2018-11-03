import time
from math import sqrt, factorial

times = 35


def fib_recursive(n):
    """
    The Fibonacci sequence as a generator:
        f(n) = f(n-1) + f(n-2)
        1, 1, 2, 3, 5, 8, 13, 21, 34…
    """
    if n <= 1:
        return n
    else:
        return fib_recursive(n-1) + fib_recursive(n-2)


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
        # Credits to Stack Overflow for this succinct version of the Fibonacci sequence.
        value = ((1+sqrt(5))**i-(1-sqrt(5))**i)/(2**i*sqrt(5))
    print(f"No function time for Fibonacci: {time.clock() - init}")

    init = time.clock()
    result = fib_recursive(times)
    print(f"Function time for Fibonacci: {time.clock() - init}")

    init = time.clock()
    factorial(times)
    print(f"No function time for factorial: {time.clock() - init}")

    init = time.clock()
    result = factorial_recursive(times)
    print(f"Function time for factorial: {time.clock() - init}")

# Standard Python interpreter results:
# No function time for Fibonacci: 7.107942644800277e-05
# Function time for Fibonacci: 3.1865595943568525
# No function time for factorial: 3.414295593362482e-06
# Function time for factorial: 2.1727335597354624e-06

# pypy interpreter results:
# No function time for Fibonacci: 0.00536044408190833
# Function time for Fibonacci: 0.18236652897743708
# No function time for factorial: 8.473660882230005e-05
# Function time for factorial: 3.290139390169089e-05
