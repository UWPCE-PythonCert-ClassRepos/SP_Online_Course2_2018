"""
Module provides a basic calculator
"""


from .exceptions import InsufficientOperands


class Calculator():
    """
    Calculator class for providing basic calculator functions
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Inserts operand on stack
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        Base calculation function
        """
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Addition function
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Subtraction function
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Multiplication function
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Division function
        """
        return self._do_calc(self.divider)
