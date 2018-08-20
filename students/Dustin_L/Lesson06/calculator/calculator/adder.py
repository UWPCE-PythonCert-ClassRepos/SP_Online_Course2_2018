"""adder Module

Contains a single Adder class that provides addition functionality
"""


class Adder(object):
    """This class performs a single static addition calculation"""

    @staticmethod
    def calc(operand_1, operand_2):
        """Performs addition of the two passed operands

        Args:
            operand_1 (float): first operand
            operand_2 (float): second operand

        Returns:
            float: result of addition of the two operands
        """
        return operand_1 + operand_2
