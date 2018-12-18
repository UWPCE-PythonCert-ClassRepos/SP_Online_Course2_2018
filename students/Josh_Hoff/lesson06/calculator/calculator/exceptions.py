"""
This module hold exceptions for the calculator
"""


class InsufficientOperands(Exception):
    """
    This exception alerts the user to put more numbers into the stack
    """
    print('Not enough numbers')


class DivideByZero(Exception):
    """
    This exception alerts the user to avoid dividing by zero
    """
    print('Cannot divide by Zero')
