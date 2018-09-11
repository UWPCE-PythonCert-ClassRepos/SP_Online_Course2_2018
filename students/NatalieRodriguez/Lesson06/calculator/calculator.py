#calculator.py

"""this structure is called dependency injection"""


from .exceptions import InsufficientOperands


class Calculator():

    """combines the modules into a calculator"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):

        """takes two arguments from the user"""

        self.stack.insert(0, number)

    def _do_calc(self, operator):

        """does the calculation"""

        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):

        """calls the addition module"""

        return self._do_calc(self.adder)

    def subtract(self):

        """calls the subtraction module"""

        return self._do_calc(self.subtracter)

    def multiply(self):

        """calls the multiplication module"""

        return self._do_calc(self.multiplier)

    def divide(self):

        """calls the division module"""

        return self._do_calc(self.divider)

