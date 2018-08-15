#!/usr/bin/env python3

"""Contains the Calculator class"""

from .exceptions import InsufficientOperands


class Calculator():

    """Integrates the other math modules into a functional calculator"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):

        """Accepts user input for the data"""

        self.stack.insert(0, number)

    def _do_calc(self, operator):

        """Runs the calculation"""

        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):

        """Calls the adder module class"""

        return self._do_calc(self.adder)

    def subtract(self):

        """Calls the subtractor module class"""

        return self._do_calc(self.subtracter)

    def multiply(self):

        """Calls the multiplier module class"""

        return self._do_calc(self.multiplier)

    def divide(self):

        """Calls the divider module class"""

        return self._do_calc(self.divider)
