"""subtractor Module

Contains a single Subtractor class that provides subtraction functionality
"""


class Subtracter(object):
    """This class performs a single static subtraction calculation"""

    @staticmethod
    def calc(operand_1, operand_2):
        """Performs subtraction of the two passed operands

        Args:
            operand_1 (float): first operand
            operand_2 (float): second operand

        Returns:
            float: result of subtraction of the two operands
        """
        return operand_1 - operand_2
