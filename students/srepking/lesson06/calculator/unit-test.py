"""Test suite for calculator."""

from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands
from calculator.exceptions import StackError


class AdderTests(TestCase):

    def test_adding(self):
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):

    def test_subtracting(self):
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))

class DivideTests(TestCase):

    def test_dividing(self):
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, -1):
                self.assertEqual(i/j, divider.calc(i, j))

        for i in range(-10, 10):
            for j in range(1, 10):
                self.assertEqual(i/j, divider.calc(i, j))

        with self.assertRaises(ZeroDivisionError):
            divider.calc(10, 0)

class MultiplyTests(TestCase):

    def test_multiply(self):
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i*j, multiplier.calc(i, j))


class CalculatorTests(TestCase):

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()
        self.calculator = Calculator(self.adder, self.subtracter, self.multiplier, self.divider)

    def test_enter_number(self):
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.assertEqual(1, self.calculator.stack[-1])
        self.assertEqual(2, self.calculator.stack[-2])

    def test_insufficient_operands(self):
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        self.adder.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()
        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()
        self.subtracter.calc.assert_called_with(1, 2)

    def test_divider_call(self):
        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()
        self.divider.calc.assert_called_with(1, 2)

    def test_multiplier_call(self):
        self.multiplier.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()
        self.multiplier.calc.assert_called_with(1, 2)

    def test_enter_one_number(self):
        self.calculator.enter_number(1)
        with self.assertRaises(InsufficientOperands):
            self.calculator.subtract()

    def test_stackError(self):
        self.calculator.enter_number(1)
        self.calculator.enter_number(1)

        with self.assertRaises(StackError):
            self.calculator.enter_number(1)

    def test_bonus(self):
        self.subtracter.calc = MagicMock(return_value=0)
        self.calculator.enter_number(2)
        self.calculator.enter_number(3)
        self.calculator.add()
        self.calculator.enter_number(1)
        self.calculator.subtract()
        self.subtracter.calc.assert_called_with(5, 1)
