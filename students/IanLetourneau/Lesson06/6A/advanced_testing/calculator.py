#!/usr/bin/env python3
# Ian Letourneau
# 10/5/2018

"""
This module combines all function modules and creates a calculator that
can utilize them.
"""

from advanced_testing.exceptions import InsufficientOperands


class Calculator(object):
    """ A class object to combine all smaller functions into one large calculator
    that functions much the same as a real-world calculator."""

    def __init__(self, adder, subtracter, multiplier, divider):
        """Initialization of smaller modules and calculator 'stack'."""
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Inputs numbers into calculator stack in order to perform
        calculations on in later function calls."""
        if len(self.stack) > 0:
            self.stack.insert(len(self.stack), number)
        else:
            self.stack.insert(0, number)

    def _do_calc(self, operator):
        """Applies calculation to stack of numbers based on where function
        was called from."""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Calls _do_calc from the adder class."""
        return self._do_calc(self.adder)

    def subtract(self):
        """Calls _do_calc from the subtracter class."""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Calls _do_calc from the multiplier class."""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Calls _do_calc from the divider class."""
        return self._do_calc(self.divider)
