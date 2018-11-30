"""
This module provides a calculator
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """Class implementing the calculation."""
    def __init__(self, adder, subtracter, multiplier, divider):
        """This method initiates."""
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """This method accepts number"""
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        """This method do calc"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """This method adds"""
        return self._do_calc(self.adder)

    def subtract(self):
        """This method subtracts"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """This method multiplies"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """This method divides"""
        return self._do_calc(self.divider)
