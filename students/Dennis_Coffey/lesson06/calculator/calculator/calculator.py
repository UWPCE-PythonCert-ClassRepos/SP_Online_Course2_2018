"""
This module implements a calculator
"""

from .exceptions import InsufficientOperands


class Calculator():
    """
    Class that implements a calculator, which allows user
    to call various calculator operations
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        """
        Specify the addition, subtraction, multiplication, and division
        classes for use by the calculator.
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider
        self.stack = []

    def enter_number(self, number):
        """ Function to pass in numbers"""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """Performs the calculation.
        operator: defines the type of calculation to perform.
        result: returns value after calculation performed"""
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Returns addition of last two numbers in calculator stack"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Returns subtraction of last two numbers in calculator stack"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Returns multiplication of last two numbers in calculator stack"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Returns division of last two numbers in calculator stack"""
        return self._do_calc(self.divider)
    