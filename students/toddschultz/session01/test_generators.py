from generators import sum_gen, double_gen, fib_gen, prime_gen

def test_sum_gen():
	sums = sum_gen(2,4,6,8)
	for i in sums:
		assert i is 20

def test_double_gen():
	doubles = list(double_gen(9))
	assert doubles[-2] is 128

def test_fib_gen():
	fibs = list(fib_gen(10))
	assert len(fibs) is 8

def test_prime_gen():
	primes = list(prime_gen(20))
	assert primes[-1] is 19