"""defines divider objects"""


class Divider:
    """defines basic divider object"""

    @staticmethod
    def calc(operand_1: float, operand_2: float):
        """performs division of two numerators with first input being numerator and
        second input denomenator
        args:
            operand_1: numerator float input
            operand_2: denomenator float input
        returns:
            float from division of operand_1/operand_2
        """
        return operand_1/operand_2
