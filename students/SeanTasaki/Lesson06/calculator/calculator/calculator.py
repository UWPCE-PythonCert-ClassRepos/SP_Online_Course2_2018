'''A Standard Calculator module'''


import logging
from .exceptions import InsufficientOperands


class Calculator():
    '''basic calculator'''

    def __init__(self, adder, subtracter, multiplier, divider):
        '''initialize'''
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    logging.basicConfig(level=logging.DEBUG)

    def enter_number(self, number):
        '''take a number'''
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        '''calculator function'''
        try:
            logging.debug("Operands: {}, {}".format(self.stack[1],
                                                    self.stack[0]))
            result = operator.calc(self.stack[1], self.stack[0])
            logging.debug("Operations: {}, Answer: {}".
                          format(operator.__class__.__name__, result))
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        '''addition'''
        return self._do_calc(self.adder)

    def subtract(self):
        '''subtraction'''
        return self._do_calc(self.subtracter)

    def multiply(self):
        '''multiplication'''
        return self._do_calc(self.multiplier)

    def divide(self):
        '''division'''
        return self._do_calc(self.divider)
