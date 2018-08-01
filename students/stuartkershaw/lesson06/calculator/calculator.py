"""
This module provides a calculator
"""


from .exceptions import InsufficientOperands

class Calculator():
    """
    This class provides calculator methods
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        This method inserts operands to the stack
        """

        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        This method ensures operands and returns result
        """

        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        This method sets addition
        """

        return self._do_calc(self.adder)

    def subtract(self):
        """
        This method sets subtraction
        """

        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        This method sets multiplication
        """

        return self._do_calc(self.multiplier)

    def divide(self):
        """
        This method sets division
        """

        return self._do_calc(self.divider)
