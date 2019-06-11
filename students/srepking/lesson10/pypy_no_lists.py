""""Instead of using comprehensions and range to call the generators and
create a list, we will use a while loop until a certain number size is reached.
We will use the largest number in the lists that pypy_vs_python.py created, and
then compare the speed from this file to the pypy_vs_python.py file."""

import time
import cProfile
import pstats

#my_list = list(range(1000))
times = 1000
double_limit = 5357543035931336604742125245300009052807024058527668037218751941851755255624680612465991894078479290637973364587765734125935726428461570217992288787349287401967283887412115492710537302531185570938977091076523237491790970633699383779582771973038531457285598238843271083830214915826312193418602834034688
fib_limit = 43466557686937456435688527675040625802564660517371780402481729089536555417949051890403879840079255169295922593080322634775209689623239873322471161642996440906533187938298969649928516003704476137795166849228875
prime_limit = 7919


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
for t in range(times):
    doublerdo = doubler()
    doubler_seq = []
    next_num = next(doublerdo)
    while next_num <= double_limit:
        doubler_seq.append(next_num)
        next_num = next(doublerdo)
#print(doubler_seq)
print('Last Double # is: ', doubler_seq[-1])
print("Doubler took: %s" % (time.perf_counter() - init))
pr_double.disable()  # stop the profiler
stats_double = pstats.Stats(pr_double)  # create stats instance
stats_double.print_stats()  # print the statistics from profiler

## Beginning of Fibonacci Code
pr_fib = cProfile.Profile()
pr_fib.enable()
init = time.perf_counter()
for t in range(times):
    fibber = fib()
    fibber_list = []
    next_num = next(fibber)
    while next_num <= fib_limit:
        fibber_list.append(next_num)
        next_num = next(fibber)
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
    primer = prime()
    prime_list = []
    next_num = next(primer)
    while next_num <= prime_limit:
        prime_list.append(next_num)
        next_num = next(primer)
print('Last prime # is: ', prime_list[-1])
print("Prime took: %s" % (time.perf_counter() - init))
pr_prime.disable()  # stop profiler
stats_prime = pstats.Stats(pr_prime)  # create stats instance
stats_prime.print_stats()  # print the stats from profiler


## Beginning of Prime_New Code with square root limiting range
pr_prime_new = cProfile.Profile()  # create profiler instance
pr_prime_new.enable()  # start profiler
primer_n = prime_new()
init = time.perf_counter()
for t in range(times):
    primer_n = prime_new()
    prime_n_list = []
    next_num = next(primer_n)
    while next_num <= prime_limit:
        prime_n_list.append(next_num)
        next_num = next(primer_n)
print('Last prime_new # is: ', prime_n_list[-1])
print("Prime Search limited by Square Root took: %s"
      % (time.perf_counter() - init))
pr_prime_new.disable()  # stop profiler
stats_prime_new = pstats.Stats(pr_prime_new)  # create stats instance
stats_prime_new.print_stats()  # print the stats from profiler
