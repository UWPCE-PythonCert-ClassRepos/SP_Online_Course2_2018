"""
ORIGINAL AUTHOR: INSTRUCTOR
CO-AUTHOR: Micah Braun
PROJECT NAME: unit-test.py
DATE CREATED: File originally created by instructor, date unknown
UPDATED: 10/18/2018
PURPOSE: Lesson 6
DESCRIPTION: Tests for Calculator class and its methods.
"""

from unittest import TestCase
from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator


class ModuleTests(TestCase):

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
