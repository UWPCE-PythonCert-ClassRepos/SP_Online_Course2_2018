import unittest
from generator import Generator

class TestGenerator(unittest.TestCase):

    gen_class = Generator()

    def test_sum_of_integers(self):
        int_list = range(0,6)
        actual_sum_list = TestGenerator.gen_class.sum_of_integers(int_list)
        expected_sum_list = [0,1,3,6,10,15]
        self.assertEqual(list(actual_sum_list), expected_sum_list)

if __name__ == '__main__':
    unittest.main() 
