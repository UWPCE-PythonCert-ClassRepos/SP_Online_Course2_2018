"""Exceptions for calculator"""


class InsufficientOperands(Exception):
    """Error when insufficient operators are in stack."""


class StackError(Exception):
    """Error when too many operators are in stack."""
