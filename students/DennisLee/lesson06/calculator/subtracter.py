"""
This module provides a subtraction operator.
"""


class Subtracter(object):
    """Class implementing the subtract calculation."""
    @staticmethod
    def calc(operand_1, operand_2):
        """
        Return the subtraction of the previous stack number by the
        number most recently entered.
        """
        return operand_2 - operand_1
