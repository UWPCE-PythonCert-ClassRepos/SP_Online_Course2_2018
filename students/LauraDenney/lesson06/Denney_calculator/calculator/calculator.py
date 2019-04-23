'''
This module provides a calculator to do operations on operands
'''


from .exceptions import InsufficientOperands


class Calculator():
    '''creates object for doing calculations'''
    def __init__(self, adder, subtracter, multiplier, divider):
        '''initiates object with instance attributes'''
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        '''inserts provided number into calculator stack at 0'''
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        '''uses unique calculator per operand to perform calculation.self
        adds result to stack as only value, and returns result
        '''
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        '''calls _do_calc with self.adder'''
        return self._do_calc(self.adder)

    def subtract(self):
        '''calls _do_calc with self.subtracter'''
        return self._do_calc(self.subtracter)

    def multiply(self):
        '''calls _do_calc with self.multiplier'''
        return self._do_calc(self.multiplier)

    def divide(self):
        '''calls _do_calc with self.divider'''
        return self._do_calc(self.divider)
