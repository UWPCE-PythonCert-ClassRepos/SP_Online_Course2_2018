import time
import cProfile
import pstats

my_list = list(range(1000))
times = 1000

def intsum():
    startval = 0
    while True:
        yield startval
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
    """This was my first attempt at calculating Prime. The methods were
    slow, and the profiler wasn't identifying anything that was obviously
    causing the slowdown. All of the time was taken in the 'Prime()' function.
    """
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
            yield next_num
            next_num = next(num_gen)

def prime_new():
    """ Every composite number (number that is not prime) has a factor
    less than or equal to its square root. Therefore, we can search only,
    up to this square root, and if a factor is not found, the number is
    prime. What is interesting to note looking at the profiler between
    the prime_new function and the prime() function is that the builtins.next
    were called the same amount. This means that the number generator
    was called the exact same amount of time for both of these functions.
    All of the time savings is presumably due to the factor that prime_new()
    is creating a much smaller range of numbers because it is only searching up
    to the square root of the number being evaluated for being prime.
    Interesting and unexpected to me!"""

    num_gen = intsum()
    next_num = next(num_gen)
    while next_num < 2:
        next_num = next(num_gen)
    yield 2
    next_num = next(num_gen)
    while True:
        for i in range(2, int(next_num ** 0.5) + 1):
            if (next_num % i) == 0:
                next_num = next(num_gen)
                break
        else:
            yield next_num
            next_num = next(num_gen)



pr_double = cProfile.Profile()  # create profiler instance
pr_double.enable()  # start profiler
init = time.perf_counter()
doublerdo = doubler() #initiate the generator
for t in range(times):
    doubler_seq = [next(doublerdo) for x in my_list]
    doublerdo = doubler()
    #print(doubler_seq)
print('Last Double # is: ', doubler_seq[-1])
print("Doubler took: %s" % (time.perf_counter() - init))
pr_double.disable()  # stop the profiler
stats_double = pstats.Stats(pr_double)  # create stats instance
stats_double.print_stats()  # print the statistics from profiler

## Beginning of Fibonacci Code
pr_fib = cProfile.Profile()
pr_fib.enable()
fibber = fib()
init = time.perf_counter()
for t in range(times):
    fibber_list = [next(fibber) for x in my_list]
    fibber = fib()
    #print(fibber_list)
print('Last Fibonacci # is: ', fibber_list[-1])
print("Fibonacci took: %s" % (time.perf_counter() - init))
pr_fib.disable()
stats_fib = pstats.Stats(pr_fib)
stats_fib.print_stats()


## Beginning of Prime Code
pr_prime = cProfile.Profile() # create profiler instance
pr_prime.enable()  # start profiler
primer = prime()
init = time.perf_counter()
for t in range(times):
    prime_list = [next(primer) for x in my_list]
    primer = prime()
    #print(prime_list)
print('Last prime # is: ', prime_list[-1])
print("Prime took: %s" % (time.perf_counter() - init))
pr_prime.disable()  # stop profiler
stats_prime = pstats.Stats(pr_prime)  # create stats instance
stats_prime.print_stats()  # print the stats from profiler


## Beginning of Prime_New Code with square root limiting range
pr_prime_new = cProfile.Profile() # create profiler instance
pr_prime_new.enable()  # start profiler
primer_n = prime_new()
init = time.perf_counter()
for t in range(times):
    prime_n_list = [next(primer_n) for x in my_list]
    primer_n = prime_new()
    #print(prime_n_list)
#print('Last prime_new # is: ', prime_n_list[-1])
print("Prime Search limited by Square Root took: %s"
      % (time.perf_counter() - init))
pr_prime_new.disable()  # stop profiler
stats_prime_new = pstats.Stats(pr_prime_new)  # create stats instance
stats_prime_new.print_stats()  # print the stats from profiler



