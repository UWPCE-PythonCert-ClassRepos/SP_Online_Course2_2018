#!/usr/bin/env python3
# Ian Letourneau
# 10/5/2018

"""
This module tests all calculator modules and expected outputs.
"""

from unittest import TestCase
from unittest.mock import MagicMock

from adder import Adder
from subtracter import Subtracter
from multiplier import Multiplier
from divider import Divider
from calculator import Calculator
from exceptions import InsufficientOperands


class AdderTests(TestCase):
    """Object to store Adder tests"""

    def test_adding(self):
        """Test adding functionality"""
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    """Object to store Subtracter tests"""

    def test_subtracting(self):
        """Test subtracter functionality"""
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class MultiplierTests(TestCase):
    """Onject to store multiplier tests"""

    def test_multiplying(self):
        """Test multiplier functionality"""
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):
    """Object to store divider tests"""

    def test_dividing(self):
        """Test diider functionalty"""
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                if i == 0 or j == 0:
                    continue
                else:
                    self.assertEqual(i / j, divider.calc(i, j))


class CalculatorTests(TestCase):
    """Object to store calculator tests"""

    def setUp(self):
        """Setup function to add modules to calculator"""
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(
            self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        """Function to raise exception if not enough
        operands are entered"""
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        """Function to run through adder calls"""
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        """Function to run through subtracter calls"""
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1, 2)

    def test_multiplier_call(self):
        """Function to run through multiplier calls"""
        self.multiplier.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(1, 2)

    def test_divider_call(self):
        """Function to run through divider calls"""
        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(1, 2)


class ModuleTests(TestCase):
    """Object to hold module tests"""

    def test_modules(self):
        """Function to test each of the modules and function calls"""

        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(5)
        calculator.enter_number(2)

        calculator.multiply()

        calculator.enter_number(46)

        calculator.add()

        calculator.enter_number(8)

        calculator.divide()

        calculator.enter_number(1)

        result = calculator.subtract()

        self.assertEqual(6, result)
