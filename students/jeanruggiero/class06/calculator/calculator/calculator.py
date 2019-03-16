"""
Define a calculator class that accepts numbers into a stack and
applies operands to the top two numbers on the stack.
"""

from .exceptions import InsufficientOperands


class Calculator():
    """
    Calculator class performs operations on two numbers as defined
    by the provided operator classes.
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        """
        Init method for calculator class takes the following
        instances of operator class methods.
        :param adder: instance of Adder class
        :param subtracter: instance of Subtracter class
        :param multiplier: instance of Multiplier class
        :param divider: instance of Devider class
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Enter the provided number into the calculator stack.
        :param number: number to push onto stack
        """
        self.stack.append(number)

    def _do_calc(self, operator):
        """
        Apply operator to the top two numbers on the stack:
        item_n-1 (operator) item_n
        :param operator: instance of Adder, Subtracter, Multiplier,
            Divider
        """
        try:
            result = operator.calc(self.stack[-2], self.stack[-1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Add the top two numbers on calculator stack.
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Subtract the top two numbers on calculator stack.
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Multiply the top two numbers on calculator stack.
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Divide top two numbers on calculator stack.
        """
        return self._do_calc(self.divider)
