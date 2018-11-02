import math

def intsum():
    i = sum = 0
    while True:
        sum += i
        i += 1
        yield sum


def intsum2():
    i = sum = 0
    while True:
        sum += i
        i += 1
        yield sum


def doubler():
    i = sum = 1
    while True:
        yield i
        i = i * 2


def fib():
    i, j = 0, 1
    while True:
        i, j = j, i + j
        yield i

def prime():
     n = 1
     # see if n is divisible by any number up to the square root of n
     while True:
        prime = False
        while not prime:
            n += 1                     
            cnt = [i for i in range(2, int(math.sqrt(n)) + 1) if n % i == 0]
            if not cnt: prime = True
        yield n
