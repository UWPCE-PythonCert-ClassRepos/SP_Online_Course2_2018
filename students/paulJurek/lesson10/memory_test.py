""" this tests out the profiling mechanism for memory usage
and tests different ways to contain random numbers.
Main goal is to see difference between set and list comparison"""


import random
range_low = int(1)
range_high = int(100000)
# at 1000000 we get 30mb and at 10000000 we get 300mb.
# seems to be linear increase using range
samples = int(range_high / 2)

@profile
def create_random_numbers():
    return random.sample(range(range_low, range_high), samples)

@profile
def create_random_sets():
    """creates a set of random numbers generated with loop"""
    setOfNumbers = set()
    while len(setOfNumbers) < samples:
        setOfNumbers.add(random.randint(range_low, range_high))
    return setOfNumbers

if __name__ == '__main__':
    random_numbers = create_random_numbers()
    random_numbers_set = create_random_sets()

"""from modifying the length we can see both methods scale linearly with
memory usage.  The radom.sample is more efficent though.  In the output
for loops each loop is only counted in increment but total includes all loops. 
This can be a bit confusing when evaluating output results

run below to get this to work
python -m memory_profiler memory_test.py
"""
