"""
This contains our Calculator Class
"""


from .exceptions import InsufficientOperands


class Calculator(object):
    """ Creating the calculator class"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """ Defining our enter number function"""
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        """ Defining our calculation function"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """ Defining our add function"""
        return self._do_calc(self.adder)

    def subtract(self):
        """ Defining our subtract function"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """ Defining our multiply function"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """ Defining our divide function"""
        return self._do_calc(self.divider)
