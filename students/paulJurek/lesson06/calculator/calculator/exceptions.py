"""defines custom exceptions for calculaotr"""


class InsufficientOperands(Exception):
    """catch when operation called with too few inputs"""
    def __init__(self):
        Exception.__init__(self, "Not enough operands in calculator")
