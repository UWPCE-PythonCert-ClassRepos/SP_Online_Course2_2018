from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands

class AdderTests(TestCase):

    def test_adding(self):
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):

    def test_subtracting(self):
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class CalculatorTests(TestCase):

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter, self.multiplier, self.divider)

    def test_multiplier(self):
        lis = [1,2,3,4,5,6,7,8,9,10,11,12]
        answers = [1,4,9,16,25,36,49,64,81,100,121,144]
        index = 0
        for nums in enumerate(lis, 1):
            x, y = nums
            self.calculator.enter_number(x)
            self.calculator.enter_number(y)
            result = self.calculator.multiply()
            self.assertEqual(answers[index], result)
            index += 1
    
    def test_divider(self):
        lis = [1,4,9,16,25,36,49,64,81,100,121,144]
        answers = [1,2,3,4,5,6,7,8,9,10,11,12]
        index = 0
        for nums in enumerate(lis, 1):
            x, y = nums
            self.calculator.enter_number(y)
            self.calculator.enter_number(x)
            result = self.calculator.divide()
            self.assertEqual(answers[index], result)
            index += 1

    def test_insufficient_operands(self):
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1, 2)

if __name__ == "__main__":
    pass