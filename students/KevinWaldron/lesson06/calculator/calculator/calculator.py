"""
This module defines the calculator class
"""


from .exceptions import InsufficientOperands


class Calculator():
    """
    Defines a calculator that supports addition, subtraction, multiplication,
    and division.  Operands are supplied via dependancy injection.
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Allows user to at a number to the operand stack
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Adds the operands on the stack
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Subtracts the operands on the stack
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Multiplies the operands on the stack
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Divides the operands on the stack
        """
        return self._do_calc(self.divider)
