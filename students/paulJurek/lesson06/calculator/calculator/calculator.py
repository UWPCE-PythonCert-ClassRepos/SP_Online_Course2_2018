"""defines calculator object"""

from .exceptions import InsufficientOperands


class Calculator:
    """defines calculator object"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number: float):
        """adds number to stack
        args:
            number: number input
        return:
            None
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """sets add method with adder"""
        return self._do_calc(self.adder)

    def subtract(self):
        """sets subtract method with subracter"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """sets method with multiplier"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """sets divide method call with divider"""
        return self._do_calc(self.divider)
