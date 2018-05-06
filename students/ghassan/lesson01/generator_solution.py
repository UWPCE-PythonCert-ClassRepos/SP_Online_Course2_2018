def intsum(i=0, total=0):
    while True:
        total += i
        yield total
        i += 1


def doubler(i=1):
    while True:
        yield i
        i *= 2


def fib(a=1, b=1):
    while True:
        yield a
        a, b = b, a + b


def prime(i=2):
    while True:
        if not [x for x in range(2, i) if i % x == 0]:
            yield i
        i += 1
