"""
module for calculator
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """ class for calculator """

    def __init__(self, adder, subtracter, multiplier, divider):
        """ initializes operators for calculator and stack for operands """

        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """ appends number to operand stack """

        self.stack.append(number)

    def _do_calc(self, operator):
        """ performs generalized calc method for different operators """

        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """ performs add operation """

        return self._do_calc(self.adder)

    def subtract(self):
        """ performs subtract operation """

        return self._do_calc(self.subtracter)

    def multiply(self):
        """ performs multiply operation """

        return self._do_calc(self.multiplier)

    def divide(self):
        """ performs division operation """

        return self._do_calc(self.divider)
