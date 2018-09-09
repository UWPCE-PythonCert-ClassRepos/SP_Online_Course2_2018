from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


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
                self.assertEqual(j - i, subtracter.calc(i, j))

class MultiplierTests(TestCase):

    def test_multiplying(self):
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):

    def test_dividing(self):
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                if i != 0:
                    self.assertEqual(j / i, divider.calc(i, j))
                # Division by zero error occurs, which clears the stack
                # and sets the current number to 0.
                else:
                    self.assertEqual(0, divider.calc(i, j))


class CalculatorTests(TestCase):

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(
                self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(2, 1)

    def test_subtracter_call(self):
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(2, 1)

    def test_multiplier_call(self):
        self.multiplier.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(2, 1)

    def test_divider_call(self):
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

class ModuleTests(TestCase):

    def setUp(self):
        self.calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

    def test_module(self):

        self.calculator.enter_number(5)
        self.calculator.enter_number(2)

        self.calculator.multiply()

        self.calculator.enter_number(46)

        self.calculator.add()

        self.calculator.enter_number(8)

        self.calculator.divide()

        self.calculator.enter_number(1)

        result = self.calculator.subtract()

        self.assertEqual(6, result)

    def test_after_division_by_zero(self):
        self.calculator.enter_number(15)
        self.calculator.enter_number(5)
        self.calculator.enter_number(3)
        self.calculator.divide()
        with self.assertRaises(InsufficientOperands):
            self.calculator.subtract()
