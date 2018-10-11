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


def fib():
    """
    The Fibonacci sequence as a generator:
        f(n) = f(n-1) + f(n-2)
        1, 1, 2, 3, 5, 8, 13, 21, 34…
    """


def prime():
    """
    Generate the prime numbers (numbers only divisible by them self and 1):
        2, 3, 5, 7, 11, 13, 17, 19, 23…
    """
