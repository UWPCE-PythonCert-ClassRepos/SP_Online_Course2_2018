"""exception method used if insufficient operators are used"""
from exceptions import InsufficientOperands

class Calculator():
    """Calculator collects numbers and calculator methods to peform calc functions"""
    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """enter operand 1 and 2 for calculation"""
        self.stack.insert(len(self.stack), number)

    def __do_calc(self, operator):
        """peforms calculation of called operator"""

        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """add method"""
        return self.__do_calc(self.adder)

    def subtract(self):
        """subtract method"""
        return self.__do_calc(self.subtracter)

    def multiply(self):
        """multiply method"""
        return self.__do_calc(self.multiplier)

    def divide(self):
        """divide method"""
        return self.__do_calc(self.divider)
