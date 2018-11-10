"""implement a simple calculator."""
from .exceptions import InsufficientOperands


class Calculator(object):
    """implement a simple calculator class."""

    def __init__(self, adder, subtracter, multiplier, divider):
        """initialize calculator class."""
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """add instructions on the operations stack"""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """performs add, subtract, multiply or divide calculation."""
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """adds two values."""
        return self._do_calc(self.adder)

    def subtract(self):
        """subtracts two values."""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """multiplies two values."""
        return self._do_calc(self.multiplier)

    def divide(self):
        """divides two values."""
        return self._do_calc(self.divider)
