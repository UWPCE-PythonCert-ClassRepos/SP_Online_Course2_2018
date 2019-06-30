from unittest import TestCase
from unittest.mock import MagicMock

from adder import Adder
from subtracter import Subtracter
from divider import Divider
from multiplier import Multiplier
from calculator import Calculator
from exceptions import InsufficientOperands

class AdderTests(TestCase):

    def test_adding(self):
        adder = Adder()

        for i in range(-10,10):
            for j in range(-10,10):
                self.assertEqual(i+j, adder.calc(i,j))

class SubtracterTests(TestCase):

    def test_subtracter(self):
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10,10):
                self.assertEqual(i-j, subtracter.calc(i,j))

class MultiplierTests(TestCase):

    def test_multiplier(self):
        multiplier = Multiplier()

        for i in range(-10,10):
            for j in range(-10,10):
                self.assertEqual(i*j, multiplier.calc(i,j))

class DividerTests(TestCase):

    def test_divider(self):
        divider = Divider()

        for i in range(-10,10):
            for j in range(1,10):
                self.assertEqual(i/j, divider.calc(i,j))

class CalculatorTests(TestCase):

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()
    
    def test_adder_call(self):
        self.adder.calc = MagicMock(return_value = 0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1,2)


    def test_subtracter_call(self):
        self.subtracter.calc = MagicMock(return_value = 0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1,2)


    def test_divider_call(self):
        self.divider.calc = MagicMock(return_value = 0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(1,2)

    def test_multiplier_call(self):
        self.multiplier.calc = MagicMock(return_value = 0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(1,2)

class ModuleTest(TestCase):

    def test_module(self):

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