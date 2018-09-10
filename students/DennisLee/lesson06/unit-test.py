"""
This module tests the `Calculator` class and its supporting classes and
exception.
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
    """Test the `Adder` class functionality."""
    def test_adding(self):
        """
        Make sure the `Adder` class produces the correct value.
        """
        adder = Adder()
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    """Test the `Subtracter` class functionality."""
    def test_subtracting(self):
        """
        Make sure the `Subtracter` class produces the correct value.
        """
        subtracter = Subtracter()
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(j - i, subtracter.calc(i, j))


class MultiplierTests(TestCase):
    """Test the `Multiplier` class functionality."""
    def test_multiplying(self):
        """
        Make sure the `Multiplier` class produces the correct value.
        """
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):
    """Test the `Divider` class functionality."""
    def test_dividing(self):
        """
        Make sure the `Divider` class produces the correct value and
        raises the correct exception when a division by zero is tried.
        """
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                if i != 0:
                    self.assertEqual(j / i, divider.calc(i, j))
                else:
                    with self.assertRaises(ZeroDivisionError):
                        self.assertEqual(j / i, divider.calc(i, j))


class CalculatorTests(TestCase):
    """Test specific single operations within the calculator."""
    def setUp(self):
        """
        Fill the calculator object with proper adder, subtracter,
        multiplier, and divider classes.
        """
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(
            self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        """
        Make sure an exception for insufficient operands is raised if
        there is only one number in the calculator stack before an
        operation is requested.
        """
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        """
        Make sure the add operation is invoked with the correct
        numbers and order.
        """
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(2, 1)

    def test_subtracter_call(self):
        """
        Make sure the subtract operation is invoked with the correct
        numbers and order.
        """
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(2, 1)

    def test_multiplier_call(self):
        """
        Make sure the multiply operation is invoked with the correct
        numbers and order.
        """
        self.multiplier.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(2, 1)

    def test_divider_call(self):
        """
        Make sure the divide operation is invoked with the correct
        numbers and order.
        """
        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(2, 1)

    def test_divide_by_zero(self):
        """
        Returns zero (with cleared stack and error message) if a
        division by zero is attempted.
        """
        self.calculator.enter_number(15)
        self.calculator.enter_number(5)
        self.calculator.enter_number(0)
        result = self.calculator.divide()
        self.assertEqual(result, 0)
