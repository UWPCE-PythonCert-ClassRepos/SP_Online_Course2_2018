"""
Calculator Class: calls calculator features
"""

from .exceptions import InsufficientOperands


class Calculator():
    """
    enter_number: appends integer to stack list
    _do_calc: call specified calculation class
    add: calc on adder class
    subtract: calc on subtracter class
    multiply: calc on multiplier class
    divide: calc on divider class
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider
        self.stack = []

    def enter_number(self, number):
        """ appends integer to stack list """
        if len(self.stack) == 2:
            self.stack.pop(0)  # limit 2 operands
        self.stack.append(number)  # fix for positional error

    def _do_calc(self, operator):
        """ call specified calculation class """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """ calc on adder class """
        return self._do_calc(self.adder)

    def subtract(self):
        """ calc on subtracter class """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """ calc on multiplier class """
        return self._do_calc(self.multiplier)

    def divide(self):
        """ cacl on divider class """
        return self._do_calc(self.divider)
