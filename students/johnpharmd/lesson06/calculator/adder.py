"""
Simple module that provides class instances for addition operations
"""


class Adder():
    """This class has only a static calc method that
       returns the result of addition of two operands
    """
    @staticmethod
    def calc(operand_1, operand_2):
        """Adds first, second operands, and returns sum"""
        return operand_1 + operand_2
