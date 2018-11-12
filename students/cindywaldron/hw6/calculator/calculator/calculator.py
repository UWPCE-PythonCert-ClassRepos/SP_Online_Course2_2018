"""Calculator module"""


from .exceptions import InsufficientOperands


class Calculator():
    """class Calculator"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """enter a number"""

        self.stack.insert(0, number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """method add"""

        return self._do_calc(self.adder)

    def subtract(self):
        """substraction"""

        return self._do_calc(self.subtracter)

    def multiply(self):
        """multiplication"""

        return self._do_calc(self.multiplier)

    def divide(self):
        """division"""

        return self._do_calc(self.divider)
