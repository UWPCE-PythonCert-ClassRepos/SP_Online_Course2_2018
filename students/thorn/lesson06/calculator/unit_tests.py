from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class AdderTests(TestCase):
    """ Tests for addition. """
    def test_adding(self):
        """ Accuracy test. """
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    """ Tests for subtraction. """
    def test_subtracting(self):
        """ Accuracy test. """
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class MultiplierTests(TestCase):
    """ Tests for multiplication. """
    def test_multiplying(self):
        """ Accuracy test. """
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):
    """ Tests for division. """
    def test_dividing(self):
        """ 
        Accuracy test.  Note: this skips 0 instead of being fitted to raise
        an exception. 
        """
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                # Skip dividing by 0 or add exception
                if j == 0:
                    continue
                self.assertEqual(i / j, divider.calc(i, j))


class CalculatorTests(TestCase):
    """ 
    Tests for calculator specific functionality.
    """
    def setUp(self):
        """ 1 time setup with modules """

        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter,
                                     self.multiplier, self.divider)

    def test_insufficient_operands(self):
        """ Test for appropriate raising of InsufficientOperands exception. """
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        """ Test for adder call having appropriate values and order. """
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()
        # Numbers are inserted at index 0.  Either switch this or switch the
        # calc function call order.
        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        """ Test for subtracter call having appropriate values and order. """
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1, 2)

    def test_multiplier_call(self):
        """ Test for multiplier call having appropriate values and order. """
        self.multiplier.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(1, 2)

    def test_divider_call(self):
        """ Test for divider call having appropriate values and order. """
        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(1, 2)
