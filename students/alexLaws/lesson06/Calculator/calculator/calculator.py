"""
This Module provides a calculator that uses the 4 main math functions
"""


from .exceptions import InsufficientOperands


class Calculator(object):
    """
    Calculator Object
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Input a number for calculations
        """
        self.stack.append(number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Call the addition module
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Call the subtraction module
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Call the multiplication module
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Call the division module
        """
        return self._do_calc(self.divider)
