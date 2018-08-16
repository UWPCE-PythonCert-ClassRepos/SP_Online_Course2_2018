"""Calculator Function"""


from .exceptions import InsufficientOperands


class Calculator(object):
    """Calculator function"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Enters a number to the stack"""

        self.stack.append(number)

    def _do_calc(self, operator):
        """Attempts to do a calculation with two numbers in stack"""

        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Performs Add Calculation"""

        return self._do_calc(self.adder)

    def subtract(self):
        """Performs Subtract Calculation"""

        return self._do_calc(self.subtracter)

    def multiply(self):
        """Performs Multiply Calculation"""

        return self._do_calc(self.multiplier)

    def divide(self):
        """Performs Divide Calculation"""

        return self._do_calc(self.divider)
