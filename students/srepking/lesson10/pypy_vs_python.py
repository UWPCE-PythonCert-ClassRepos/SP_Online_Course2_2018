import time

my_list = list(range(100))
times = 10000

def intsum():
    def intsum_init():
        return 0
    startval = intsum_init()
    while True:
        val = (yield startval)
        if val == 'restart':
            startval = intsum_init()
        else:
            startval += 1


def intsum2():
    start_val1 = 0
    int_gen = intsum()
    while True:
        next_int = next(int_gen)
        yield start_val1+next_int
        start_val1 = start_val1+next_int


def doubler():
    start_val1 = 1
    while True:
        yield start_val1
        start_val1 = start_val1 * 2



def fib():
    start_val1 = 1
    start_val2 = 1
    yield 1
    yield 1
    while True:
        next_num = start_val1 + start_val2
        yield next_num
        start_val1 = start_val2
        start_val2 = next_num


def prime():
    def prime_init():
        num_gen.send('restart')
    num_gen = intsum()
    next_num = next(num_gen)
    while next_num < 2:
        next_num = next(num_gen)
    yield 2
    next_num = next(num_gen)
    while True:
        for i in range(2, next_num):
            if (next_num % i) == 0:
                next_num = next(num_gen)
                break
        else:
            val = (yield next_num)
            if val == 'restart':
                prime_init()
                num_gen = intsum()
                next_num = next(num_gen)
            else:
             next_num = next(num_gen)


def factorial(num):
    fact = 1
    for i in range(1, num+1):
        fact = fact * i
    return fact





init = time.perf_counter()
doublerdo = doubler() #initiate the generator
for t in range(times):
    doubler_seq = [next(doublerdo) for x in my_list]
    doublerdo = doubler()
    #print(doubler_seq)
print("Doubler took: %s" % (time.perf_counter() - init))

## Beginning of Fibonacci Code
fibber = fib()
init = time.perf_counter()
for t in range(times):
    fibber_list = [next(fibber) for x in my_list]
    fibber = fib()
    #print(fibber_list)
print("Fibonacci took: %s" % (time.perf_counter() - init))


primer = prime()
init = time.perf_counter()
for t in range(times):
    prime_list = [next(primer) for x in my_list]
    #prime.send('restart')
    primer = prime()
    #print(prime_list)
print("Prime took: %s" % (time.perf_counter() - init))

init = time.perf_counter()
for t in range(times):
    factorial_list = [factorial(x) for x in my_list]
    #print(factorial_list)
print("Factorial took: %s" % (time.perf_counter() - init))
