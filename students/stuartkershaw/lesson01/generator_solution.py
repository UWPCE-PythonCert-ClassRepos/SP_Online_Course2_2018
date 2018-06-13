def intsum(i=0, cur=0):
    while True:
        cur += i
        yield cur
        i += 1


def intsum2(i=0, cur=0):
    while True:
        cur += i
        yield cur
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
    prime_nums = set()
    while True:
        for p in prime_nums:
            if i % p == 0:
                break
        else:
            prime_nums.add(i)
            yield i
        i += 1
