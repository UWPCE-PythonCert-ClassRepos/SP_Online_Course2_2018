"""This module contains the calculator class."""

from .exceptions import InsufficientOperands


class Calculator:
    """This class use to instantiate a calculator."""

    def __init__(self, adder, subtracter, multiplier, divider):
        """Initialize the calculator."""
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Enter number into stack."""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """Private method for different operator call."""
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Add two numbers."""
        return self._do_calc(self.adder)

    def subtract(self):
        """Subtract two numbers."""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Multiple two numbers."""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Divide two numbers."""
        return self._do_calc(self.divider)
