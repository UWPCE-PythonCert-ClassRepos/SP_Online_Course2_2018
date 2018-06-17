from math import sqrt

def intsum():
    result, increment = 0, 1
    while True:
        yield result
        result += increment
        increment += 1

def intsum2():
    result = 0
    while True:
        yield result * (result + 1) / 2
        result += 1

def doubler():
    result = 1
    while True:
        yield result
        result *= 2

def fib():
    x, y = 0, 1
    while True:
        x, y = y, x + y
        yield x

def prime():
    result = 1
    while True:
        result += 1
        for i in range(int(sqrt(result)), 1, -1):
            if not result % i:
                break
        else:
            yield result