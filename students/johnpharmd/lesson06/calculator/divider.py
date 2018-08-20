"""
Simple module that provides class instances for division operations
"""


class Divider():
    """This class has only a static calc method that
       returns the result of division of two operands
    """
    @staticmethod
    def calc(operand_1, operand_2):
        """Divides first operand by second operand, and returns quotient"""
        return operand_1/operand_2
