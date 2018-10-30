"""
This module provides a calculator
"""
from .exceptions import InsufficientOperands


class Calculator(object):
    """
    Calculator object definition
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        """
        Calculator object initialization
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Insert the input to the stack - FIFO
        """
        # self.stack.insert(0, number)
        self.stack.append(number)

    def _do_calc(self, operator):
        """
        Perform operation defined by operator,
        for the first 2 elements of the stack.
        """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Return the sum of the first 2 elements of self.stack
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Return the result of subtraction of the first 2 elements of self.stack
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Return the result of multiplication of the first 2 elements
        of self.stack
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Return the result of division of the first 2 elements of self.stack
        """
        return self._do_calc(self.divider)
