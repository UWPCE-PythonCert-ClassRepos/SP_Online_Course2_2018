"""Calculates"""


from .exceptions import InsufficientOperands

from .exceptions import StackError


class Calculator:
    """Calculator class"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider
        self.stack = []

    def enter_number(self, number):
        """Inserts number to top of stack"""
        if len(self.stack) >= 2:
            raise StackError
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """Calls operator class to perform desired operation."""
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Returns sum of [A,B] A+B."""
        return self._do_calc(self.adder)

    def subtract(self):
        """Returns difference of [A,B] A-B."""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Returns product of [A,B] A*B."""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Returns dividend of [A,B] A/B."""
        return self._do_calc(self.divider)
