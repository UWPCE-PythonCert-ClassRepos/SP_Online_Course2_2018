"""
Provides a simple calculator using injected methods
"""

from .exceptions import InsufficientOperands


class Calculator():
    """
    Calculator object
    """
    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Appends number for calculation"""
        self.stack.append(number)

    def _do_calc(self, operator):
        """Performs requested calculation"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """calls adder function"""
        return self._do_calc(self.adder)

    def subtract(self):
        """calls subtracter function"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """calls mulitplier function"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """calls divider function"""
        return self._do_calc(self.divider)
