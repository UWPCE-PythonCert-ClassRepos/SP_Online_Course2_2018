#unit_test.py

"""this tests the entire calculator module"""


from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class AdderTests(TestCase):

    """ this tests Adder"""

    def test_adding(self):
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))

class SubtracterTests(TestCase):

    """ this tests Subtractor"""

    def test_subtracting(self):
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class MultiplierTests(TestCase):

    """this tests Multiplier"""

    def test_multiplier(self):

        """ test multiplier"""

        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):

    """ this tests Divider"""

    def test_divider(self):
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                if j != 0:
                    self.assertEqual(i / j, divider.calc(i, j))


class CalculatorTests(TestCase):

    """ runs all tests"""

    def setUp(self):

        """ setup"""

        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):

        """ test insufficient operands"""

        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):

        """ test adder"""

        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):

        """ test subtracter"""

        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1, 2)

    def test_multiplier_call(self):

        """ test multiplier"""

        self.multiplier.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(1, 2)

    def test_divider_call(self):

        """ test divider"""

        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(1, 2)
