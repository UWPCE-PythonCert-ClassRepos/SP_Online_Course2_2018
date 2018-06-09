"""
InsufficientOperands Exception and the Calculator class
"""


class InsufficientOperands(Exception):
    """
    Create the InsufficientOperands exception for use in Calculator.
    """
    pass


class Calculator(object):
    """
    Create the calculator object.
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        """
        Initialize the calculator
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider
        self.stack = []

    def enter_number(self, num):
        """
        Insert the input to the front of self.stack
        """
        self.stack.insert(0, num)

    def _do_calc(self, operator):
        """
        Return result of the operation of the first 2 elements of self.stack
        """
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def subtract(self):
        """
        Return the difference of the first 2 elements of self.stack
        """
        return self._do_calc(self.subtracter)

    def add(self):
        """
        Return the sum of the first 2 elements of self.stack
        """
        return self._do_calc(self.adder)

    def multiply(self):
        """
        Return the product of the first 2 elements of self.stack
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Return the quotient of the first 2 elements of self.stack
        """
        return self._do_calc(self.divider)
