"""
Calculator module that contains Calculator class
"""

from .exceptions import InsufficientOperands


class Calculator():
    """Define a Calculator class"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Insert a number into self.stack"""
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        """Do calculations with the provided operator"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Add two numbers"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Subtract one number from another"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Multiply one number by another"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Divide one number by another"""
        return self._do_calc(self.divider)
