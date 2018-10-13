'''
Module to create a calculator
'''

from .exceptions import InsufficientOperands


class Calculator(object):
    '''
    Create a calculator object with functionality:
    add, subtract, multiply, divide
    '''

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        ''' User inputs a number into the calculator '''
        self.stack.append(number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        ''' Call the addition class '''
        return self._do_calc(self.adder)

    def subtract(self):
        ''' Call the subtraction class '''
        return self._do_calc(self.subtracter)

    def multiply(self):
        ''' Call the multiplication class '''
        return self._do_calc(self.multiplier)

    def divide(self):
        ''' Call the division class '''
        return self._do_calc(self.divider)
