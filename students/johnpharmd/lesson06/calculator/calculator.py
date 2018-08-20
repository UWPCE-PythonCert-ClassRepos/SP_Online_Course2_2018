"""
This module creates a calculator stack with input functionality for two
operands and performs numeric operations on first operand by second operand
"""
from exceptions import InsufficientOperands


class Calculator():
    """
    This class provides a stack for two operands and
    has a general calc method that uses instances from
    numeric operation classes to perform an operation on the
    first operand in the stack by the second operand
    """
    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Enables input of number into stack"""
        # choice of 0 for insert position is incorrect because it
        # leads to incorrect subtraction and division results
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Calls calc method of Adder class instance"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Calls calc method of Subtracter class instance"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Calls calc method of Multiplier class instance"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Calls calc method of Divider class instance"""
        return self._do_calc(self.divider)
