''' My Digital Calculator. '''

from .exceptions import InsufficientOperands

class Calculator():
    ''' Base class '''

    def __init__(self, adder, subtracter, multiplier, divider):
        ''' Initializer '''
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        ''' inserts a new number in the second position '''
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        ''' Execute operations with the proper operator and catches InsufficientOperands '''
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        ''' returns numbers added '''
        return self._do_calc(self.adder)

    def subtract(self):
        ''' returns numbers subtracted '''
        return self._do_calc(self.subtracter)

    def multiply(self):
        ''' returns numbers multiplied '''
        return self._do_calc(self.multiplier)

    def divide(self):
        ''' returns numbers divided '''
        return self._do_calc(self.divider)
