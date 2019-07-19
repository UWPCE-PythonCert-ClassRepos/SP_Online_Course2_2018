"""
Student: Jared Mulholland
Assignment: Calculator Unit Tests
Date: 7/17/2019
"""

from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.divider import Divider
from calculator.multiplier import Multiplier
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands

class AdderTests(TestCase):
    """tests for adder method"""

    def test_adding(self):
        """confirm adder returns expected result"""
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i+j, adder.calc(i,j))

class SubtracterTests(TestCase):
    """tests for subtractor method"""
    def test_subtracter(self):
        """confirm subtracter returns expected result"""
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i-j, subtracter.calc(i,j))

class MultiplierTests(TestCase):
    """tests for multiplier method"""
    def test_multiplier(self):
        """confirm multiplier returns expected result"""
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i*j, multiplier.calc(i,j))

class DividerTests(TestCase):
    """tests for divider method"""
    def test_divider(self):
        """confirm divider returns expected result"""
        divider = Divider()

        for i in range(-10, 10):
            for j in range(1, 10):
                self.assertEqual(i/j, divider.calc(i,j))

class CalculatorTests(TestCase):
    """Tests for calculator method"""

    def setUp(self):
        """setup for calculator tests"""
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        """tests insuffucient operands is raised when only one number entered"""
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()
    
    def test_adder_call(self):
        """tests adder method is called correctly"""
        self.adder.calc = MagicMock(return_value = 0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1,2)


    def test_subtracter_call(self):
        """tests subtracter method is called correctly"""
        self.subtracter.calc = MagicMock(return_value = 0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1,2)


    def test_divider_call(self):
        """tests divider method is called correctly"""
        self.divider.calc = MagicMock(return_value = 0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(1,2)

    def test_multiplier_call(self):
        """tests multiplier method is called correctly"""
        self.multiplier.calc = MagicMock(return_value = 0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(1,2)