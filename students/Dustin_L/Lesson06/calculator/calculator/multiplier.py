"""multiplier Module

Contains a single Multiplier class that provides multiplication functionality.
"""


class Multiplier(object):
    """This class performs a single static mutliplication calculation"""

    @staticmethod
    def calc(operand_1, operand_2):
        """Performs multiplication of the two passed operands

        Args:
            operand_1 (float): first operand
            operand_2 (float): second operand

        Returns:
            float: result of multiplication of the two operands
        """
        return operand_1*operand_2
