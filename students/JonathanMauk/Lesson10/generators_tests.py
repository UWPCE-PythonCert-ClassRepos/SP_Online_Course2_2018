import math
import time

times = 1000


def fib(n):
    """
    The Fibonacci sequence as a generator:
        f(n) = f(n-1) + f(n-2)
        1, 1, 2, 3, 5, 8, 13, 21, 34…
    """
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)


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


if __name__ == "__main__":

    init = time.clock()
    for i in range(times):
        # Credits to Stack Overflow for this succinct version of the Fibonacci sequence.
        value = ((1+sqrt(5))**i-(1-sqrt(5))**i)/(2**i*sqrt(5))
    print(f"No function time for Fibonacci: {time.clock() - init}")

    init = time.clock()
    fib(times)
    print(f"Function time for Fibonacci: {time.clock() - init}")

    init = time.clock()
    math.factorial(times)
    print(f"No function time for factorial: {time.clock() - init}")

    init = time.clock()
    factorial(times)
    print(f"Function time for factorial: {time.clock() - init}")
