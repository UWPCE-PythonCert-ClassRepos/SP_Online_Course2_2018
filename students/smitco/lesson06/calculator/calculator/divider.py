"""Divides two numbers"""


class Divider():
    """Class for divider"""

    @staticmethod
    def calc(operand_1, operand_2):
        """Perform division"""
        try:
            return operand_1/operand_2
        except ZeroDivisionError:
            return False
