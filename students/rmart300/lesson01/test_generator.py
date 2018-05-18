import unittest
from generator import Generator

class TestGenerator(unittest.TestCase):

    gen_class = Generator()

    def test_sum_of_integers(self):
        int_list = range(0,6)
        actual_sum_list = TestGenerator.gen_class.sum_of_integers(int_list)
        expected_sum_list = [0,1,3,6,10,15]
        self.assertEqual(list(actual_sum_list), expected_sum_list)

    def test_doubler(self):
        start = 0
        stop = 6
        actual_double_list = TestGenerator.gen_class.doubler(0,6)
        expected_double_list = [1,2,4,8,16]
        self.assertEqual(list(actual_double_list), expected_double_list)

    def test_fibonacci(self):
        int_list = range(1,8)
        actual_fib_list = TestGenerator.gen_class.fibonacci(int_list)
        expected_fib_list = [1,1,2,3,5,8,13]
        self.assertEqual(list(actual_fib_list),expected_fib_list)

    def test_prime(self):
        int_list = range(0,20)
        actual_prime_list = TestGenerator.gen_class.prime(int_list)
        expected_prime_list = [2,3,5,7,11,13,17,19]
        self.assertEqual(list(actual_prime_list),expected_prime_list)

if __name__ == '__main__':
    unittest.main() 
