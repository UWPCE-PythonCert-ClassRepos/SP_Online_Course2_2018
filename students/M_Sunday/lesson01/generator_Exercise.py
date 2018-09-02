

def intsum(i=0, sum=0):
    while True:
        sum += i
        i += 1
        yield sum


def intsum2(i=0, sum=0):
    while True:
        sum += i
        i += 1
        yield sum


def doubler(i=1):
    while True:
        yield i
        i = i*2


def fib(prev=1, curr=1):
    while True:
        yield prev
        futu = curr + prev
        prev = curr
        curr = futu


def prime(active=2, prime=True):
    while True:
        for int in range(2, active):
            if active % int == 0:
                prime = False
            else:
                pass
        if prime:
            yield active
        active += 1
        prime = True
