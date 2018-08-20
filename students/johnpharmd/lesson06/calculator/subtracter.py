"""
Simple module that provides class instances for subtraction operations
"""


class Subtracter():
    """This class has only a static calc method that
       returns the result of subtraction of two operands
    """
    @staticmethod
    def calc(operand_1, operand_2):
        """Subtracts second operand from first operand; returns difference"""
        return operand_1 - operand_2
