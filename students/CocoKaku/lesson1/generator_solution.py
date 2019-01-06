def intsum():
    """
    keep adding the next integer
    0 + 1 + 2 + 3 + 4 + 5 + …
    so the sequence is:
    0, 1, 3, 6, 10, 15 …
    """
    sum = 0
    n = 1
    while True:
        yield sum
        sum += n
        n += 1


def intsum2():
    """

    :return:
    """
    pass


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
    n = 1
    nminus1 = 1
    nminus2 = 0
    while True:
        yield n
        n = nminus1 + nminus2
        nminus2 = nminus1
        nminus1 = n


def isPrime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
    return True


def prime():
    n = 2
    while True:
        while not isPrime(n):
            n += 1
        yield n
        n += 1