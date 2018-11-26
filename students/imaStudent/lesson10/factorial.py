from memory_profiler import profile
from datetime import datetime
import random

random.seed(datetime.now())


# implements an inline factorial function
@profile(precision=4)
def inline_factorial(n):
    x = 1
    for i in range(n, 0, -1):
        x = x * i
    return x


# implements a recursive factorial function
@profile()
def recursive_factorial(n):
    return 1 if (n < 1) else n * recursive_factorial(n-1)


# implements a memory use random number generator for largest number
@profile
def memory_use_test(number):
    nums = [random.randint(0, number) for x in range(100000)]
    largest = max(nums)
    return largest


num = memory_use_test(5)
print("inline factorial {} = {}".format(num, inline_factorial(num)))
print("recursive factorial {} = {}".format(num, recursive_factorial(num)))
