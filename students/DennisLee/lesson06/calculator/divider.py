"""
This module provides a division operator.
"""


class Divider(object):
    """Class implementing the divide calculation."""
    @staticmethod
    def calc(operand_1, operand_2):
        """
        Return the division of the previous stack number by the number
        most recently entered.
        """
        return operand_2 / operand_1
