from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


def main():

    adder = Adder()
    subtracter = Subtracter()
    multiplier = Multiplier()
    divider = Divider()

    calculator = Calculator(adder, subtracter, multiplier, divider)
    return calculator

if __name__ == "__main__":
    cal = main()
    cal.enter_number(5)
    cal.enter_number(7)
    print(cal.multiply())