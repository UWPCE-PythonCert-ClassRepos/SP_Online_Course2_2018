

"""This module implements a calculator,
stores the operands into a call stack"""


from .exceptions import InsufficientOperands


class Calculator():
    """Implementation of a calculator object"""

    def __init__(self, adder, subtracter, multiplier, divider):
        """Initializes the object based on the parameters passed in"""
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Appends a number into the call stack"""
        self.stack.append(number)

    def _do_calc(self, operator):
        """Attempts to operate on two numbers"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Calls the adder module"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Calls the subtracter module"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Calls the multiplier module"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Calls the divider module"""
        return self._do_calc(self.divider)
