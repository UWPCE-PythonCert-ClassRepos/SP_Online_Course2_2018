from unittest import TestCase

from adder import Adder
from subtracter import Subtracter
from multiplier import Multiplier
from divider import Divider
from calculator import Calculator


class ModuleTests(TestCase):

    def test_module(self):
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(3)
        calculator.enter_number(4)

        self.assertEqual(12, calculator.multiply())

        calculator.enter_number(2)

        self.assertEqual(10, calculator.subtract())

        calculator.enter_number(10)

        self.assertEqual(calculator.add(), 20)

        calculator.enter_number(5)

        result = calculator.divide()

        self.assertEqual(4, result)
