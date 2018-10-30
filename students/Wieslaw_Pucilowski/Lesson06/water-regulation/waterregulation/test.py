"""
Unit tests for the water-regulation module
"""
__author__ = "Wieslaw Pucilowski"
import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider

ACTIONS = {
    'PUMP_IN': Pump.PUMP_IN,
    'PUMP_OFF': Pump.PUMP_OFF,
    'PUMP_OUT': Pump.PUMP_OUT
}


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    # def test_dummy(self):
    #     """
    #     Just some example syntax that you might use
    #     """
    #     pump = Pump('127.0.0.1', 8000)
    #     pump.set_state = MagicMock(return_value=True)
    #
    #     self.fail("Remove this test.")

    def test_decider(self):
        """
        Unit test for decider
        :return:
        """
        decider = Decider(100, .1)

        test1 = decider.decide(75, ACTIONS['PUMP_OFF'], ACTIONS)
        test2 = decider.decide(125, ACTIONS['PUMP_OFF'], ACTIONS)
        test3 = decider.decide(106, ACTIONS['PUMP_OFF'], ACTIONS)
        test4 = decider.decide(105, ACTIONS['PUMP_IN'], ACTIONS)
        test5 = decider.decide(85, ACTIONS['PUMP_IN'], ACTIONS)
        test6 = decider.decide(95, ACTIONS['PUMP_OUT'], ACTIONS)
        test7 = decider.decide(105, ACTIONS['PUMP_OUT'], ACTIONS)
        self.assertEqual(ACTIONS['PUMP_IN'], test1)
        self.assertEqual(ACTIONS['PUMP_OUT'], test2)
        self.assertEqual(ACTIONS['PUMP_OFF'], test3)
        self.assertEqual(ACTIONS['PUMP_OFF'], test4)
        self.assertEqual(ACTIONS['PUMP_IN'], test5)
        self.assertEqual(ACTIONS['PUMP_OFF'], test6)
        self.assertEqual(ACTIONS['PUMP_OUT'], test7)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick(self):
        """
        Testing the tick method in controller
        :return:
        """
        decider = Decider(100, .1)
        pump = Pump('127.0.0.1', '8080')
        sensor = Sensor('127.0.0.1', '8081')
        controller = Controller(sensor, pump, decider)

        sensor.measure = MagicMock(return_value=95)
        pump.get_state = MagicMock(return_value=pump.PUMP_IN)
        decider.decide = MagicMock(return_value=pump.PUMP_IN)
        pump.set_state = MagicMock(return_value=True)

        controller.tick()

        sensor.measure.assert_called_with()
        pump.get_state.assert_called_with()
        decider.decide.assert_called_with(95, pump.PUMP_IN, ACTIONS)
