"""
This module tests the calculator
"""
from .exceptions import InsufficientOperands


class Calculator:
    """
    Calculator module
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        """
        Initialization
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider
        self.stack = []

    def enter_number(self, number):
        """
        Seek user input
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        Perform operation
        """
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Instruct calculator to perform addition
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Instruct calculator to perform subtraction
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Instruct calculator to perform multiplication
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Instruct calculator to perform divsion
        """
        return self._do_calc(self.divider)
