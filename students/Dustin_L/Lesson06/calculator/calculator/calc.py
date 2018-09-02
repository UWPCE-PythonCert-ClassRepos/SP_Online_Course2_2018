"""calc Module

Contains the Calculator class
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """This class provides calculator functionality

    Raises:
        InsufficientOperands: Raised when not enough operands are available for
                              a calculation.
    """
    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def _do_calc(self, operator):
        """Performs the operation provided by the passed operator

        Args:
            operator (operator): Object with a "calc" method.

        Raises:
            InsufficientOperands: Raised when not enough operands are available
                                  for a caculation.

        Returns:
            float: result of operation.
        """
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def enter_number(self, number):
        """Adds a number to the calculator's operation stack

        Args:
            number (float): value to be added to operation stack
        """
        self.stack.insert(0, number)

    def add(self):
        """Performs addition operation on the top two values in the operation
           stack.

        Returns:
            float: result of addition.
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """Performs subration operation on the top two values in the operation
           stack.

        Returns:
            float: result of subtraction.
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Performs multiplication operation on the top two values in the
           operation stack.

        Returns:
            float: result of multiplication.
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """Performs divide operation on the top two values in the operation
           stack.

        Returns:
            float: result of divide.
        """
        return self._do_calc(self.divider)
