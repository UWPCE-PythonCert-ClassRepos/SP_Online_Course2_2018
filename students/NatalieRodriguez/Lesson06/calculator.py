#calculator.py

#this structure is called dependency injection

class Calculator(object):

    def __init__(self, adder, subtracter, multiplier, divider):
        self.Adder = adder
        self.Subtracter = subtracter
        self.Multiplier = multiplier
        self.Divider = divider

        self.stack = []

    def enter_number(self, number):
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        result = self.Adder.calc(self.stack[0], self.stack[1])

        self.stack = [result]
        return result

    def add(self):
        return self._do_calc(self.Adder)

    def subtract(self):
        return self._do_calc(self.Subtracter)

    def multiply(self):
        return self._do_calc(self.Multiplier)

    def divide(self):
        return self._do_calc(self.Divider)

