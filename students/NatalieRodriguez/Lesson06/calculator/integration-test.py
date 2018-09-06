#integration_test.py

'''this tests the integration of all files'''


from unittest import TestCase
from unittest.mock import MagicMock

from adder import Adder
from subtracter import Subtracter
from multiplier import Multiplier
from divider import Divider
from calculator import Calculator
from exceptions import InsufficientOperands


class ModuleTests(TestCase):

    def test_module(self):

        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(7)
        calculator.enter_number(3)

        calculator.multiply()

        calculator.enter_number(24)

        calculator.add()

        calculator.enter_number(5)

        calculator.divide()

        calculator.enter_number(1)

        result = calculator.subtract()

        self.assertEqual(8, result)