"""
Student: Jared Mulholland
Assignment: Calculator Integrated Tests
Date: 7/18/2019
"""


from unittest import TestCase

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.divider import Divider
from calculator.multiplier import Multiplier
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class ModuleTest(TestCase):
    """Tests for integrated functionality of classes"""
    def test_module(self):
        """Test that calculator performs operations as expected"""
        
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