"""
Exception definitions for the Calculator class.
"""


class InsufficientOperands(Exception):
    """
    Exception to indicate there are too few operands on the calculator
    stack to perform the requested operation.
    """
