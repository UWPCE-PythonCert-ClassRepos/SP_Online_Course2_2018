"""
This is Caclulator
"""
from .exceptions import InsufficientOperands


class Calculator(object):
    """calculator operations"""

    def __init__(self, adder, subtracter, multiplier, divider):
        """Initialize"""

        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Takes a number"""
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        """Do calculation"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Add"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Subtract"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Multiply"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Divide"""
        return self._do_calc(self.divider)
