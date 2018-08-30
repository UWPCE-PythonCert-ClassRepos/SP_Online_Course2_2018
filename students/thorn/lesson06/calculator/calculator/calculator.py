"""
Calculator module containing the calculator class.
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """
    A more complex calculator.  Takes external modules and uses them
    to perform calculations.
    """
    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Inserts a new operand to index 0 of the operand stack.
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        Performs the appropriate calculation passed into this function through
        an operator object.

        Raises an InsufficientOperands error if there are <2 operands in the
        stack.
        """
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """ Adds first 2 values in the operand stack. """
        return self._do_calc(self.adder)

    def subtract(self):
        """ Subtracts first 2 values in the operand stack. """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """ Mutliplies first 2 values in the operand stack. """
        return self._do_calc(self.multiplier)

    def divide(self):
        """ Divides first 2 values in the operand stack. """
        return self._do_calc(self.divider)
