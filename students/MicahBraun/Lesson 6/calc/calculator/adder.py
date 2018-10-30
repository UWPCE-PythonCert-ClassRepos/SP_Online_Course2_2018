"""
ORIGINAL AUTHOR: INSTRUCTOR
CO-AUTHOR: Micah Braun
PROJECT NAME: adder.py
DATE CREATED: File originally created by instructor, date unknown
UPDATED: 10/18/2018
PURPOSE: Lesson 6
DESCRIPTION: Returns the calculation of adder(x + y) back to
method caller add(), which returns the calculation to method
_do_calc().
"""


class Adder:
    """
    This module provides the addition operator to the
    calculator class
    """
    @staticmethod
    def calc(operand_1, operand_2):
        """
        Performs addition operation on passed-in
        operands
        :param operand_1:
        :param operand_2:
        """
        return operand_1 + operand_2
