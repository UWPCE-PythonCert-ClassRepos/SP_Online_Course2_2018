# Generators

def doubler():
    for n in itertools.count():
        yield 2**n  

def intsum():
    for n in itertools.accumulate(itertools.count()):
        yield n

def fib():
    x = 0
    y = 1
    while True:
        yield x
        x, y = y, x + y

def prime():
    for x in itertools.count(2):
        # number is considered prime, until proven otherwise
        prime = True
        # checks modulus of all numbers under x, except 1
        for n in range(2, x):
            if x%n == 0:
                prime = False
        if prime:
            yield x
