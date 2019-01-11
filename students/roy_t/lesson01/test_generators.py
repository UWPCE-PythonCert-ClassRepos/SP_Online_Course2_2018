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


if __name__ == "__main__":
	unittest.main()