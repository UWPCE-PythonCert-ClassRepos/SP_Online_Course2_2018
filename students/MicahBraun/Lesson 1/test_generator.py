"""
test_generator.py

tests the solution to the generator lab

can be run with py.test or nosetests
"""

import generator_solution as gen


def test_intsum():
	g = gen.intsum()
	print('Sum')
	print(next(g) == 0)
	print(next(g) == 1)
	print(next(g) == 3)
	print(next(g) == 6)
	print(next(g) == 10)
	print(next(g) == 15)


# noinspection PyUnboundLocalVariable
def test_doubler():

	g = gen.doubler()
	print('\nDoubler')
	print(next(g) == 1)
	print(next(g) == 2)
	print(next(g) == 4)
	print(next(g) == 8)
	print(next(g) == 16)
	print(next(g) == 32)

	for i in range(10):
		j = next(g)

	print(j == 2 ** 15)


def test_fib():
	g = gen.fib()
	print('\nFibonacci')
	print([next(g) for i in range(9)] == [1, 1, 2, 3, 5, 8, 13, 21, 34])


def test_prime():
	print('\nPrime')
	g = gen.prime()
	for val in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
		print(next(g) == val)


if __name__ == "__main__":

	test_intsum()

	test_doubler()

	test_fib()

	test_prime()
