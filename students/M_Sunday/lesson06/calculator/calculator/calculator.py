"""
This module provides the main calculator functionality
"""


from .exceptions import InsufficientOperands


class Calculator:
    """
    This class is the base calculator class to support addition,
    subtraction, multiplication, and division
    """
    def __init__(self, adder, subtracter, multiplier, divider):
        """
        This __init__ method sets up the class instance to allow
        for quick calling to the adder(), subtracter(), multipler(),
        and divider() classes.
        :param adder:
        :param subtracter:
        :param multiplier:
        :param divider:
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        This method allows the user to enter a number onto the calculator stack
        :param number:
        :return:
        """
        if not self.stack:
            self.stack.insert(0, number)
        else:
            self.stack.insert(1, number)

    def _do_calc(self, operator):
        """
        This method actually calls the external classes for the calculator and
        allows the 'calc' method within each of those classes to perform the
        calculation.
        :param operator:
        :return:
        """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        This method adds the values within the calculator stack
        :return:
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        This method subtracts the values within the calculator stack
        :return:
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        This method multiplies the values within the calculator stack
        :return:
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        This method divides the values within the calculator stack
        :return:
        """
        return self._do_calc(self.divider)
