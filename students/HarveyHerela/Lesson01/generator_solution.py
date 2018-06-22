def intsum():
    current = 0
    sum = 0
    while True:
        sum += current
        yield sum
        current += 1


def doubler():
    current = 1
    while True:
        yield current
        current *= 2
        

def fib():
    # Fibonacci starts out as 1, 1
    yield 1
    yield 1
    cur = [1, 1]
    while True:
        the_sum = sum(cur)
        cur[0] = cur[1]
        cur[1] = the_sum
        yield the_sum
        
        
def prime():

    def is_prime(num):
        for i in range(2, num):
            if (num % i) == 0:
                return False
        return True
    
    cur = 1
    while True:
        prime = False
        while not prime:
            cur += 1
            prime = is_prime(cur)
        yield cur
