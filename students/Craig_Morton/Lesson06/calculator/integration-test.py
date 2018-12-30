"""This module tests the calculator tool as a whole."""


from unittest import TestCase
from calculator.adder import Adder as a
from calculator.subtracter import Subtracter as s
from calculator.multiplier import Multiplier as m
from calculator.divider import Divider as d
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class ModuleTests(TestCase):
    """Test the calculator module/UI during random, sustained usage."""
    def setUp(self):
        self.calculator = Calculator(a(), s(), m(), d())

    def test_module(self):
        """
        Make sure the calculator returns the correct value after a
        series of random number entries and operations.
        """
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
        """
        Make sure an insufficient operands exception occurs if a user
        immediately invokes an operation after a division by zero error
        without specifying another number. (Following a division by
        zero, the stack is cleared, and only a zero is left there.)
        """
        self.calculator.enter_number(15)
        self.calculator.enter_number(5)
        self.calculator.enter_number(0)
        self.calculator.divide()  # Div by 0 clears stack and pushes 0
        with self.assertRaises(InsufficientOperands):
            self.calculator.subtract()
        self.calculator.enter_number(8)
        result = self.calculator.subtract()
        self.assertEqual(-8, result)
