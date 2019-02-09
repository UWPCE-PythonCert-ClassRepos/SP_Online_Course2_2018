"""
Module for the calculator.
This module calls the other modules for calculations.
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """Class Calculator."""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Function for entering new numbers to the calculator from user."""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Returns the adder module to do addition."""
        return self._do_calc(self.adder)

    def subtract(self):
        """Returns the subtractor module to do addition."""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Returns the multiplier module to do addition."""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Returns the divider module to do addition."""
        return self._do_calc(self.divider)
