#!/usr/bin/env python3

__author__ = "roy_t githubtater"

import unittest
import generators as gen

class TestGenerators(unittest.TestCase):

	def test_sum_of_integers(self):
		sum_gen = gen.sum_of_integers()
		assert next(sum_gen) == 0
		assert next(sum_gen) == 1
		assert next(sum_gen) == 3
		assert next(sum_gen) == 6
		assert next(sum_gen) == 10
		assert next(sum_gen) == 15

	def test_doubler(self):
		dub_gen = gen.doubler()
		assert next(dub_gen) == 1
		assert next(dub_gen) == 2
		assert next(dub_gen) == 4
		assert next(dub_gen) == 8
		assert next(dub_gen) == 16
		assert next(dub_gen) == 32

	def test_fibonacci_sequence(self):
		fib_gen = gen.fibonacci_sequence()
		assert next(fib_gen) == 0
		assert next(fib_gen) == 1
		assert next(fib_gen) == 1
		assert next(fib_gen) == 2
		assert next(fib_gen) == 3
		assert next(fib_gen) == 5
		assert next(fib_gen) == 8
		assert next(fib_gen) == 13
		assert next(fib_gen) == 21
		assert next(fib_gen) == 34

	def test_prime_numbers(self):
		prim_gen = gen.prime_numbers()
		assert next(prim_gen) == 2
		assert next(prim_gen) == 3
		assert next(prim_gen) == 5
		assert next(prim_gen) == 7
		assert next(prim_gen) == 11
		assert next(prim_gen) == 13

	def test_squared_nums(self):
		sq_gen = gen.squared_nums()
		for i in range(1, 10):
			assert next(sq_gen) == i*i

	def test_cubed_nums(self):
		cube_gen = gen.cubed_nums()
		for i in range(1, 10):
			assert next(cube_gen) == i**3

	def test_count_by_threes(self):
		vals = [0, 3, 6, 9, 12, 15, 18]
		c = gen.count_by_threes()
		for i in range(len(vals)):
			assert next(c) == vals[i]

	def test_minus_7(self):
		vals = [0, -7, -14, -21, -28, -35, -42, -49]
		m = gen.minus_7()
		for i in range(len(vals)):
			assert next(m) == vals[i]



if __name__ == "__main__":
	unittest.main()