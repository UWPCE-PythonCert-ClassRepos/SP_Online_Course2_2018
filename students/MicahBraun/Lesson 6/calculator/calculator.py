"""
ORIGINAL AUTHOR: INSTRUCTOR
CO-AUTHOR: Micah Braun
PROJECT NAME: calculator.py
DATE CREATED: File originally created by instructor, date unknown
UPDATED: 10/18/2018
PURPOSE: Lesson 6
DESCRIPTION: Calculator.py is part of suite for Lesson 6's
calculator testing-suite reviewing TDD, Linting,Flake8, and
Coverage. The calculator class behaves as a calculator (taking
in operands and performing the four basic mathematical
operations (addition, subtraction, multiplication,
division).
"""

from calculator.exceptions import InsufficientOperands


class Calculator:
    """
    Calculator class contains constructor, operations, method
    calls for class
    """
    def __init__(self, adder, subtracter, multiplier, divider):
        """
        Calculator constructor
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Method gets number for calc
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        Method performs operations using passed-in operator
        with stack
        """
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Adder method call
        :return: result to _do_calc
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Subtracter method call
        :return: result to _do_calc
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Multiplier method call
        :return: result to _do_calc
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Multiplier method call
        :return: result to _do_calc
        """
        return self._do_calc(self.divider)
