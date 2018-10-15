from unittest import TestCase
from unittest.mock import MagicMock

from advanced_testing.adder import Adder
from advanced_testing.subtracter import Subtracter
from advanced_testing.multiplier import Multiplier
from advanced_testing.divider import Divider
from advanced_testing.calculator import Calculator
from advanced_testing.exceptions import InsufficientOperands


class ModuleTests(TestCase):
    """Object to hold modules tests"""

    def test_module(self):
        """Function to run through function calls for each module"""

        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(5)
        calculator.enter_number(2)

        calculator.multiply()

        calculator.enter_number(46)

        calculator.add()

        calculator.enter_number(8)

        calculator.divide()

        calculator.enter_number(1)

        result = calculator.subtract()

        self.assertEqual(6, result)
