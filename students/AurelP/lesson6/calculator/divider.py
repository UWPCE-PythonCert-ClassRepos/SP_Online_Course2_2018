"""
This module provides a divider operator
"""


class Divider(object):
    """
    class Divider
    """

    @staticmethod
    def calc(operand_1, operand_2):
        """calc"""
        try:
            return operand_1/operand_2
        except ZeroDivisionError as error:
            return error
