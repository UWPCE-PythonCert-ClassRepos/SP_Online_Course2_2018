def intsum(i=0, sum=0):
    while True:
        sum += i
        yield sum
        i += 1

def doubler(double=1):
    while True:
        yield double
        double *= 2

def fib(i=0, j=1):
    while True:
        yield j
        i, j = j, i + j

def gen_primes():
    D = {}
    q = 2
    
    while True:
        if q not in D:
            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        
        q += 1
