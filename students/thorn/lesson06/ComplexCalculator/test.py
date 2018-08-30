from unittest import TestCase
from unittest.mock import MagicMock

from adder import Adder
from multiplier import Multiplier
from divider import Divider
from subtracter import Subtracter

class AdderTests(TestCase):
    
    def test_adding(self):
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class CalculatorTests(TestCase):


    