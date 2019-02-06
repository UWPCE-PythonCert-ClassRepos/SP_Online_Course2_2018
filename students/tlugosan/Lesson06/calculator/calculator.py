"""
This module compasses the Calculator class
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """ This class provides the basic functionality of a calculator.

    Attributes:
        adder       (object): Instance of Adder class
        subtracter  (object): Instance of Subtracter class
        multiplier  (object): Instance of Multiplier class
        divider    (object): Instance of Divider class
        """

    def __init__(self, adder, subtracter, multiplier, divider):

        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """ This method inserts a number in the stack at position 0.

        Parameters:
            number (float): Number to be inserted in the stack
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """ Wrapper for all the 4 calculations.

        Parameters:
            operator (operator): Type of operation to be done on the numbers.

        Returns:
            number (float): The result of the operation.
        """
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        The function adds two numbers.

        Returns:
            number (float): The result of the operation.
            """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        The function subtracts two numbers.

        Returns:
            number (float): The result of the operation.
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        The function multiplies two numbers.

        Returns:
            number (float): The result of the operation.
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        The function divides two numbers.

        Returns:
            number (float): The result of the operation.
        """
        return self._do_calc(self.divider)
