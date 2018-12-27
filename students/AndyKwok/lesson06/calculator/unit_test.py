"""
This module tests individual methods within the calculator
"""
from unittest import TestCase
from unittest.mock import MagicMock

from calculator.subtracter import Subtracter
from calculator.adder import Adder
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class AdderTests(TestCase):
    """
    Class for testing adder method
    """

    def test_adding(self):
        """
        Assert adding
        """
        adder = Adder()
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    """
    Class for testing Subtracter method
    """

    def test_subtracting(self):
        """
        Assert subtracting
        """
        subtracter = Subtracter()
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class MultiplierTests(TestCase):
    """
    Class for testing Multiplier method
    """

    def test_multiplying(self):
        """
        Assert multiplying
        """
        multiplier = Multiplier()
        for i in range(0, 9):
            for j in range(0, 9):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):
    """
    Class for testing Divider method
    """

    def test_dividing(self):
        """
        Assert dividing
        """
        divider = Divider()
        for i in range(1, 9):
            for j in range(1, 9):
                self.assertEqual(i / j, divider.calc(i, j))


class CalculatorTests(TestCase):
    """
    Class for testing the calculator class
    """

    def setUp(self):
        """
        Initialization
        """
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()
        self.calculator = Calculator(self.adder,
                                     self.subtracter,
                                     self.multiplier,
                                     self.divider)

    def test_insufficient_operands(self):
        """
        Test for error
        """
        self.calculator.enter_number(0)
        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        """
        Test inputs for adder
        """
        self.adder.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()
        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        """
        Test inputs for subtracter
        """
        self.subtracter.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()
        self.subtracter.calc.assert_called_with(1, 2)

    def test_multiplier_call(self):
        """
        Test inputs for multiplier
        """
        self.multiplier.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()
        self.multiplier.calc.assert_called_with(1, 2)

    def test_divider_call(self):
        """
        Test inputs for divider
        """
        self.divider.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()
        self.divider.calc.assert_called_with(1, 2)
