"""
This module provides a calculator object
"""
from .exceptions import InsufficientOperands


class Calculator(object):
    """This class performs mathematical operations on 2 operands"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        self.stack.append(number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        return self._do_calc(self.adder)

    def subtract(self):
        return self._do_calc(self.subtracter)

    def multiply(self):
        return self._do_calc(self.multiplier)

    def divide(self):
        return self._do_calc(self.divider)
