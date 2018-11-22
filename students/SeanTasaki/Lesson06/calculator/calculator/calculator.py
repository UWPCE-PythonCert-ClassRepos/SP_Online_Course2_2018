from .exceptions import InsufficientOperands
import logging


class Calculator(object):

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    logging.basicConfig(level=logging.DEBUG)

    def enter_number(self, number):
        self.stack.insert(0, number)


    def _do_calc(self, operator):
        try:
            logging.debug("Operands: {}, {}".format(self.stack[1], self.stack[0]))
            result = operator.calc(self.stack[1], self.stack[0])
            logging.debug("Operations: {}, Answer: {}".format(operator.__class__.__name__, result))
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        return self._do_calc(self.adder)

    def subtract(self):
        return self._do_calc(self.subtracter)

    def multiply(self):
        return self._do_calc(self.multiplier)

    def divide(self):
        return self._do_calc(self.divider)


