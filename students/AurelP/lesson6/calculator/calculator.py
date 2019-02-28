"""
class Calculator
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """
    Class Calculator
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        """
        init calculator
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider
        self.stack = []

    def enter_number(self, number):
        """enter nr"""
        self.stack.append(number)

    def _do_calc(self, operator):
        """perform calculation"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands
        self.stack = [result]
        return result

    def add(self):
        """add"""
        return self._do_calc(self.adder)

    def subtract(self):
        """substract"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """multiply"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """divide"""
        return self._do_calc(self.divider)
