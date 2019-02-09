"""Module for Calculator"""

from .exceptions import InsufficientOperands


class Calculator:
    """Class to build a Calculator"""

    def __init__(self, adder, subtracter, multiplier, divider):
        """
        Initialize Calculator with basic functions
        :param adder: object for adding
        :param subtracter: object for subtracting
        :param multiplier: object for multiplying
        :param divider: object for dividing
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Enter a number into the calculator stack
        :param number: int
        :return: None
        """
        # ah ha, I found you.
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        """
        Execute the requested calculation and move result to pos 0 in stack
        :param operator: Type of calculation (add, subtact, etc.)
        :return: result
        """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
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
        """Multiply two numbers."""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Divide two numbers."""
        return self._do_calc(self.divider)
