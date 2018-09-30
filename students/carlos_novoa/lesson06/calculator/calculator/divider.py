"""
This module for Calculator division
"""


class Divider():
    """ Contains division methods """

    @staticmethod
    def calc(operand_1, operand_2):
        """ Division on two arguments, unless either arg is zero """
        if operand_1 == 0 or operand_2 == 0:
            return 0
        return operand_1 / operand_2
