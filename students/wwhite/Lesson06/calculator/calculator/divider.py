"""
This module provides a division operator
"""


class Divider(object):
    """
    Class which divides two inputs into one another
    """
    @staticmethod
    def calc(operand_1, operand_2):
        """
        Method which takes in two parameters and divides them into one another. The method returns
        zero when a 'ZeroDivisionError' occurs
        """
        try:
            return operand_1/operand_2
        except ZeroDivisionError:
            return 0
