"""
This module provides a divider operator
"""


class Divider(object):
    """This class provides an addition operator"""

    @staticmethod
    def calc(operand_1, operand_2):
        """This method takes two numbers and divides
         the first parameter to the second parameter."""
        if operand_2 == 0:
            raise ZeroDivisionError
        else:
            return operand_1 / operand_2
