"""
Hiro Lesson6 Assignment: Calculator module
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """
    Calling each mathematical operation modules
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        """
        intialize
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider
        self.stack = []

    def enter_number(self, number):
        """
        Facing users for the data entry
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        Stack operation to prepare for mathematical operations
        """
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands
        self.stack = [result]
        return result

    def add(self):
        """
        Mathematical operations: Adding
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Mathematical operations: Subtracting
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Mathematical operations: Multiplying
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Mathematical operations: Dividing
        """
        return self._do_calc(self.divider)
