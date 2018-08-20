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

        calculator.enter_number(5)
        calculator.enter_number(2)

        r1 = calculator.multiply()
        print('multiplication result:', r1)
        calculator.enter_number(46)

        r2 = calculator.add()
        print('addition result:', r2)
        calculator.enter_number(8)

        r3 = calculator.divide()
        print('division result:', r3)
        calculator.enter_number(1)

        result = calculator.subtract()
        print('result after final step of subtraction:', result)
        self.assertEqual(6, result)
