from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calc import Calculator
from calculator.exceptions import InsufficientOperands


class ModuleTests(TestCase):

    def test_module(self):

        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(5)
        calculator.enter_number(2)

        self.assertEqual(10, calculator.multiply())

        calculator.enter_number(46)

        self.assertEqual(56, calculator.add())

        calculator.enter_number(8)

        self.assertEqual(7, calculator.divide())

        calculator.enter_number(1)

        self.assertEqual(6, calculator.subtract())
