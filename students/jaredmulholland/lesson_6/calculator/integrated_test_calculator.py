
from unittest import TestCase
from unittest.mock import MagicMock



from adder import Adder
from subtracter import Subtracter
from divider import Divider
from multiplier import Multiplier
from calculator import Calculator
from exceptions import InsufficientOperands




class ModuleTest(TestCase):

    def test_module(self):

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