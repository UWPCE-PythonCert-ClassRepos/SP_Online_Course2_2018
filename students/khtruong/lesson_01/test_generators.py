#!/usr/bin/env python

import unittest
import generators as g


class GeneratorTests(unittest.TestCase):

    def test_integer_sum(self):
        gen = g.integer_sum()
        seq = [0, 1, 3, 6, 10, 15]
        for s in seq:
            self.assertEqual(next(gen), s)

    def test_doubler(self):
        gen = g.doubler()
        seq = [1, 2, 4, 8, 16, 32]
        for s in seq:
            self.assertEqual(next(gen), s)

    def test_fib(self):
        gen = g.fib()
        seq = [1, 1, 2, 3, 5, 8, 13, 21, 34]
        for s in seq:
            self.assertEqual(next(gen), s)

    def test_prime(self):
        gen = g.prime()
        seq = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        for s in seq:
            self.assertEqual(next(gen), s)

if __name__ == "__main__":
    unittest.main()
