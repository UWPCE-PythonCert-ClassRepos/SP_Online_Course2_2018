"""
Simple module that provides class instances for multiplication operations
"""


class Multiplier():
    """This class has only a static calc method that
       returns the result of multiplication of two operands
    """
    @staticmethod
    def calc(operand_1, operand_2):
        """Multiplies first operand by second operand, and returns product"""
        return operand_1*operand_2
