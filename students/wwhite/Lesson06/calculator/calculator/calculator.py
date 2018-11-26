"""
This module provides addition, subtraction, division, and
multiplication capabilities
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """
    Class with methods to add, subtract, multiply, and divide two
    parameters with one another
    """
    def __init__(self, adder, subtracter, multiplier, divider):
        """
        Initializer method to create instances of each class and
        a black list
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        This method appends to the list with an input parameter
        """
        self.stack.append(number)

    def _do_calc(self, operator):
        """
        This method us used to call the appropriate operator
        for the calculation
        """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        This method calls the addition operator
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        This method calls the subtraction operator
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        This method calls the multiplication operator
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        This method calls the division operator
        """
        return self._do_calc(self.divider)
