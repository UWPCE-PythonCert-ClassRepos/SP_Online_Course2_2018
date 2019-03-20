"""
Module which creates a calculator
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """class to implement calculator operations"""
    def __init__(self, adder, subtracter, multiplier, divider):
        """initializing method"""
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """accept number"""
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        """do calc"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """implement the adder"""
        return self._do_calc(self.adder)

    def subtract(self):
        """implement the subtracter"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """implement the multiplier"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """implement the divider"""
        return self._do_calc(self.divider)
