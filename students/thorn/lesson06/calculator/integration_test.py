"""
Integration tests to ensure the calculator and submodules come together
and work accurately.
"""

from unittest import TestCase
from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator


class ModuleTests(TestCase):
    """ Module Tests to ensure module accuracy. """
    def test_module(self):
        """ Tests each module against an expected output to ensure accuracy. """
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(5)
        calculator.enter_number(2)

        # Tests
        # Add:
        self.assertEqual(7, calculator.add())

        # Subtract:
        calculator.enter_number(5)
        self.assertEqual(2, calculator.subtract())

        # Multiply:
        calculator.enter_number(5)
        self.assertEqual(10, calculator.multiply())

        # Divide:
        calculator.enter_number(1)
        self.assertEqual(10, calculator.divide())
