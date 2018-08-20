from unittest import TestCase
from unittest.mock import MagicMock
from adder import Adder
from subtracter import Subtracter
from multiplier import Multiplier
from divider import Divider
from calculator import Calculator
from calculator import InsufficientOperands


class AdderTests(TestCase):

    def test_adding(self):
        add = Adder()
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i+j, add.calc(i, j))


class SubtracterTests(TestCase):

    def test_subbing(self):
        sub = Subtracter()
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i-j, sub.calc(i, j))


class MultiplierTests(TestCase):

    def test_multiplier(self):
        mult = Multiplier()
        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i*j, mult.calc(i, j))


class DividerTests(TestCase):

    def test_divider(self):
        div = Divider()
        for i in range(-10, 10):
            for j in [x for x in range(-10, 10) if x != 0]:
                self.assertEqual(i/j, div.calc(i, j))


class CalculatorTests(TestCase):

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter,
                                     self.multiplier, self.divider)

    def operator_call(self, operand, method):
        operand.calc = MagicMock(return_value=0)
        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        method()

        operand.calc.assert_called_with(1, 2)

    def test_insufficient_operands(self):
        self.calculator.enter_number(0)
        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder(self):
        self.operator_call(self.adder, self.calculator.add)

    def test_subber(self):
        self.operator_call(self.subtracter, self.calculator.subtract)

    def test_multiplier(self):
        self.operator_call(self.multiplier, self.calculator.multiply)

    def test_divider(self):
        self.operator_call(self.divider, self.calculator.divide)
