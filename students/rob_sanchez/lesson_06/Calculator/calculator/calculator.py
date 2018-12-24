'''' Calculator moddule that contains a Calculator class '''
from .exceptions import InsufficientOperands


class Calculator(object):
    ''' Calculator class that computes the desired
    calculation after two numbers are entered. '''

    def __init__(self, adder, subtracter, multiplier, divider):
        ''' This method initializes each of the calculation methods. '''
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        ''' Insterts the given number in the stack '''
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        ''' Returns the result of the specified calculation of
        the first two numbers in the stack'''
        try:
            result = operator.calc(self.stack.pop(), self.stack.pop())
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        ''' Returns the addition result '''
        return self._do_calc(self.adder)

    def subtract(self):
        ''' Returns the subtraction result '''
        return self._do_calc(self.subtracter)

    def multiply(self):
        ''' Returns the multiplication result '''
        return self._do_calc(self.multiplier)

    def divide(self):
        ''' Returns the division result '''
        return self._do_calc(self.divider)
