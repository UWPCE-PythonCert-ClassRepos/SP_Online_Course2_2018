"""
This module is the main python file for adding, subtracting,
multiplying, and dividing numbers
"""
from .exceptions import InsufficientOperands
from .exceptions import DivideByZero


class Calculator:
    """
    This class sets up the calculator to add, subtract, multiply, and divide.
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        """
        This method initializes the variables for the calculator
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        This appends the number to the end of the stack
        """
        self.stack.append(number)

    def _do_calc(self, operator):
        """
        This method calculates and deals with errors
        """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands
        except ZeroDivisionError:
            raise DivideByZero

        self.stack = [result]
        return result

    def add(self):
        """
        This method calls the adder
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        This method calls the subtracter
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        This method calls the multiplier
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        This method calls the divider
        """
        return self._do_calc(self.divider)
