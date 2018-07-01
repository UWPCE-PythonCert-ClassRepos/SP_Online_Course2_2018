"""
This module provides a subtraction operator
"""


class Subtracter(object):
    """
    Subtractor class
    Produces operand 1 - operand 2
    """
    @staticmethod
    def calc(operand_1, operand_2):
        """
        method to subtract operand2 from operand1
        :param operand_1: first operand (a number)
        :param operand_2: second operand (a number)
        :return: result of subtraction
        """
        return operand_1 - operand_2
