"""
This module provides unit tests for calculator
"""

from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class AdderTests(TestCase):
    """Class to test Adder"""

    def test_adding(self):
        """test for Adder"""
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    """Class to test subtracter"""

    def test_subtracting(self):
        """test for subtracting"""
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class MultiplierTests(TestCase):
    """Class to test multiplier"""

    def test_multiplying(self):
        """test for multiplier"""
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):
    """Class to test Divider"""

    def test_dividing(self):
        """ test for Divider"""
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                # skipping 0 to avoid division by zero errors
                if j == 0:
                    continue
                    # with self.assertRaises(ZeroDivisionError):
                    #     divider.calc(i, j)
                self.assertEqual(i / j, divider.calc(i, j))


class CalculatorTests(TestCase):
    """Class to test Calculator"""

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(
            self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        """tests for insufficient operands"""
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        """tests for adder call"""
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        """tests for adder call"""
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1, 2)

    def test_multiplier_call(self):
        """tests for adder call"""
        self.multiplier.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(1, 2)

    def test_divider_call(self):
        """tests for adder call"""
        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(1, 2)
