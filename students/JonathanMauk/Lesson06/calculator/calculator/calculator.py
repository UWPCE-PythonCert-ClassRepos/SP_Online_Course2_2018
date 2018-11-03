"""
Calculator module that gets operands and passes them to operation modules.
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """Calculator class."""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Method that inserts operands into stack."""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """Basic operator function."""
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands
        except ZeroDivisionError:
            result = 0

        self.stack = [result]
        return result

    def add(self):
        """Adder function."""
        return self._do_calc(self.adder)

    def subtract(self):
        """Subtracter function."""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Multiplier function."""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Divider function."""
        return self._do_calc(self.divider)
