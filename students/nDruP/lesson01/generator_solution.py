def intsum():
    isum = [0, 0]
    while True:
        yield isum[1]
        isum[0] += 1
        isum[1] += isum[0]


def intsum2(n=1):
    while True:
        yield (n*(n-1)) / 2
        n += 1


def doubler(n=0):
    while True:
        yield 2 ** n
        n += 1


def fib():
    f_n = [0, 1]
    while True:
        yield f_n[1]
        f_n[1] = sum(f_n)
        f_n[0] = f_n[1] - f_n[0]


def prime(n=2):
    prime_n = True
    while True:
        for i in range(3, n, 2):
            if n % i == 0:
                prime_n = False
                break
        if prime_n:
            yield n
        if n > 2:
            prime_n = True
            n += 2
        else:
            n += 1


def to_power(pwr=1):
    n = 0
    while True:
        yield n ** pwr
        n += 1


def count_by(factor=1):
    n = 0
    while True:
        yield n * factor
        n += 1


def factor_powers(factor=1):
    n = 0
    while True:
        yield factor ** n
        n += 1
