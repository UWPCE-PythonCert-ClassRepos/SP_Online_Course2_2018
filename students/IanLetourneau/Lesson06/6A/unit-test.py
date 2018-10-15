from unittest import TestCase
from unittest.mock import MagicMock

from advanced_testing.adder import Adder
from advanced_testing.subtracter import Subtracter
from advanced_testing.multiplier import Multiplier
from advanced_testing.divider import Divider
from advanced_testing.calculator import Calculator
from advanced_testing.exceptions import InsufficientOperands


class AdderTests(TestCase):
    """Object to store adding tests"""

    def test_adding(self):
        """Function to unittest adding function"""
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    """Object to store subtracter tests"""

    def test_subtracting(self):
        """Function to unittest subtracter function"""
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class MultiplierTests(TestCase):
    """Object to store multiplier tests"""

    def test_multiplying(self):
        """Function to unittest multiplier function"""
        multiplier = Multiplier()
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):
    """Object to store divider tests"""

    def test_divider(self):
        """Function to unittest divider function"""
        divider = Divider()
        for i in range(-10, 10):
            for j in range(-10, 10):
                if j != 0:
                    self.assertEqual(i / j, divider.calc(i, j))


class CalculatorTests(TestCase):
    """Object to store calculator test functions"""

    def setUp(self):
        """Function to add all modules into calculator object"""
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(
            self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        """Function to test exception raise for insufficient operands"""
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        """Function to test adder functionality"""
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        """Function to test subtracter functionality"""
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
