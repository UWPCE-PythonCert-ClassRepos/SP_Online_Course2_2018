"""A simple calculator."""

from .exceptions import InsufficientOperands


class Calculator(object):
    """An object to encapsulate a simple calculator."""

    def __init__(self, adder, subtracter, multiplier, divider):
        """Initializor for the calculator."""
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """API to push a # onto the calculator's stack."""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """Helper to run a calculation (e.g., add, subtract)."""
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Add operation."""
        return self._do_calc(self.adder)

    def subtract(self):
        """Subtract operation."""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Multiply operation."""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Divide operation."""
        return self._do_calc(self.divider)
