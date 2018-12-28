"""Calculate numbers"""


from .exceptions import InsufficientOperands


class Calculator():
    """Class for calculator"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Allows user to enter numbers"""
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        """Performs calculation"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Performs addition"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Performs subtraction"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Performs multiplication"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Performs division"""
        return self._do_calc(self.divider)
