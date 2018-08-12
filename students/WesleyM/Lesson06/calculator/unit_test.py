"""Test Cases to verify calculator functions"""
from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class AdderTests(TestCase):
    """Adder Test Case"""
    def test_adding(self):
        """Test case that adds from range -10 to 10"""
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    """Subtracter Test Case"""
    def test_subtracting(self):
        """Test case that subtracts from range -10 to 10"""
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class MultiplierTests(TestCase):
    """Multiplier Test Case"""
    def test_multiplying(self):
        """Test case that multiplies from range -10 to 10"""
        multiplier = Multiplier()
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):
    """Divider Test Case"""
    def test_divider(self):
        """Test case that divides from range -10 to 10"""
        divider = Divider()
        for i in range(-10, 10):
            for j in range(-10, 10):
                if j != 0:
                    self.assertEqual(i / j, divider.calc(i, j))


class CalculatorTests(TestCase):
    """Series of Calculator Tests"""
    def setUp(self):
        """Test case that setups the other test cases from range -10 to 10"""
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder,
                                     self.subtracter,
                                     self.multiplier, self.divider)

    def test_insufficient_operands(self):
        """Test insufficient operands"""
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        """Test Case Adds Two Numbers"""
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        """Test Case Subtracts Two Numbers"""
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1, 2)
