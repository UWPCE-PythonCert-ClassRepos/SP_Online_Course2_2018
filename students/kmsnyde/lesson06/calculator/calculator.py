"""create a calculator"""

from calculator.exceptions import InsufficientOperands


class Calculator():
    """calculator methods"""

    def __init__(self, adder, subtracter, multiplier, divider):
        """initializer"""
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """number entry point"""
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        """perform calculation"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """addition"""
        return self._do_calc(self.adder)

    def subtract(self):
        """subtraction"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """multiplication"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """division"""
        return self._do_calc(self.divider)
