def intsum(i=0):
    sum = 0
    while True:
        sum = sum + i
        i = i + 1
        yield sum


def intsum2(i=0):
    sum = 0
    while True:
        sum = sum + i
        i = i + 1
        yield sum


def doubler(i=1):
    while True:
        yield i
        i *= 2


def fib():
    i, j = 0, 1
    while True:
        i, j = j, i + j
        yield i


def prime(i=2):
    while True:
        if i < 2 or not [x for x in range(2, i) if i % x == 0]:
            yield i
        i += 1
