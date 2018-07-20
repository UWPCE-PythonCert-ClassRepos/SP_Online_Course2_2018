"""divider Module

Contains a single Divider class that provides divide functionality
"""


class Divider(object):
    """This class performs a single static divide calculation"""

    @staticmethod
    def calc(operand_1, operand_2):
        """Performs divide of the two passed operands

        Args:
            operand_1 (float): first operand
            operand_2 (float): second operand

        Returns:
            float: result of divide of the two operands
        """
        return operand_1/operand_2
