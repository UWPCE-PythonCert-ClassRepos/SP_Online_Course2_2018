"""
This module provides a calculator-specific exception, which is raised
whenever there are less than two numbers in the stack to perform an
operation.
"""


class InsufficientOperands(Exception):
    """
    Let the program know if there are only one or zero numbers entered
    before a calculator operation is requested.
    """
    pass
