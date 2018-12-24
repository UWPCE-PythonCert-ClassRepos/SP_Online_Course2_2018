''' This module provides the Divider operator. '''


class Divider(object):
    ''' This is the Divider class that returns
    the division of the input given '''

    @staticmethod
    def calc(operand_1, operand_2):
        ''' Returns the division of operand_1 and operand_2 '''
        try:
            return operand_1/operand_2
        except ZeroDivisionError:
            return "Can't divide by zero!"
