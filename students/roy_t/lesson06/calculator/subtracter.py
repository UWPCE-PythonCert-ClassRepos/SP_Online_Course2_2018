"""
This module provides a subtraction operator
"""


class Subtracter:
    """Class for subtracting."""

    @staticmethod
    def calc(operand_1, operand_2):
        """
        Calculate subtacting two operands.
        :param operand_1: The first operand in the stack
        :param operand_2: The second operand in the stack.
        :return: Difference between operand 1 and 2
        """
        return operand_1 - operand_2
