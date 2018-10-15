#!/usr/bin/env python3
# Ian Letourneau
# 10/5/2018

"""
This module adds two numbers together.
"""


class Adder(object):
    """Object to store adding functionality"""

    @staticmethod
    def calc(operand_1, operand_2):
        """Static method to perform adding operation"""

        return operand_1+operand_2
