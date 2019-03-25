"""
This module provodes a calculator exception if there
are less than two numbers in the stack.  Two numbers
are necessary for any of the calculations.
"""

class InsufficientOperands(Exception):
    """ Class for insufficient operands exception,
    if there are less than two numbers in stack."""
    pass
