all: primes.c primes.html

primes.c: primes.pyx setup.py
    python setup.py build_ext --inplace

primes.html: primes.pyx
    cython -a primes.pyx