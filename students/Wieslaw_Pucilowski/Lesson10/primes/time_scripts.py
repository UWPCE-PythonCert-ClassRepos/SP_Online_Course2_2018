from timeit import timeit as timer
import primes
import primes_py

repetitions = 1000
num_p = 100
print("="*70)
print("Script run time for first {} prime numbers and {} repetitions".format(num_p, repetitions))

print("primes with cython:", timer(
    'primes.primes(num_p)',
    globals=globals(),
    number=repetitions
))

print("primes only python:", timer(
    'primes_py.primes_py(num_p)',
    globals=globals(),
    number=repetitions
))