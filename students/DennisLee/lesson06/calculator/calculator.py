"""
This module implements a calculator for direct user or automated program
usage.
"""


from .exceptions import InsufficientOperands


class Calculator(object):
    """
    This class implements a calculator, which a user or an automated
    tool can use to make various numerical calculations.
    """
    def __init__(self, adder, subtracter, multiplier, divider):
        """
        Specify the addition, subtraction, multiplication, and division
        classes for use by the calculator. These classes need to have
        the corresponding operation functionality implemented in their
        `calc` methods.

        :adder:  The addition class to use.

        :subtracter:  The subtraction class to use.

        :multiplier:  The multiplication class to use.

        :divider:  The division class to use.

        :return:  The new instance of the calculator.
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Enter a number to use in an upcoming calculation. If 2+ extra
        numbers are entered into the calculator before a calculation
        operation is specified, this number will be ignored.

        :number:  The number to use.

        :return:  None.
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        Perform the calculation.

        :operator:  The class containing the desired calculation
                    operation. The class needs to have the operation
                    implemented in its `calc` method.

        :return:  The numerical result of the calculation. If a division
                  by zero is attempted, the stack is cleared, and a
                  single zero is left in the stack.
        """
        result = "Mistake"
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands
        except ZeroDivisionError:
            print("\nDivision by zero error - resetting.\n")
            result = 0

        self.stack = [result]
        return result

    def add(self):
        """
        Return the addition of the last two numbers in the calculator
        stack.

        :return:  The last two numbers added together.
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Return the subtraction of the last two numbers in the calculator
        stack.

        :return:  The value of the second-to-last value minus the last
                  value.
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Return the product of the last two numbers in the calculator
        stack.

        :return:  The value of the two numbers multiplied together.
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Return the quotient of the last two numbers in the calculator
        stack.

        :return:  The value of the second-to-last value divided by the
                  last value.
        """
        return self._do_calc(self.divider)
