"""
Unit tests for waterregulation
"""
import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider

ACTIONS = {
    'PUMP_IN': 1,
    'PUMP_OFF': 0,
    'PUMP_OUT': -1
}

class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def test_decider_decide(self):
        """
        Unit test for decider
        :return:
        """

        deciders = Decider(100, .10)
        decider_1 = deciders.decide(85, ACTIONS['PUMP_OFF'], ACTIONS)
        decider_2 = deciders.decide(115, ACTIONS['PUMP_OFF'], ACTIONS)
        decider_3 = deciders.decide(105, ACTIONS['PUMP_OFF'], ACTIONS)
        decider_4 = deciders.decide(105, ACTIONS['PUMP_IN'], ACTIONS)
        decider_5 = deciders.decide(95, ACTIONS['PUMP_IN'], ACTIONS)
        decider_6 = deciders.decide(95, ACTIONS['PUMP_OUT'], ACTIONS)
        decider_7 = deciders.decide(105, ACTIONS['PUMP_OUT'], ACTIONS)
        self.assertEqual(ACTIONS['PUMP_IN'], decider_1)
        self.assertEqual(ACTIONS['PUMP_OUT'], decider_2)
        self.assertEqual(ACTIONS['PUMP_OFF'], decider_3)
        self.assertEqual(ACTIONS['PUMP_OFF'], decider_4)
        self.assertEqual(ACTIONS['PUMP_IN'], decider_5)
        self.assertEqual(ACTIONS['PUMP_OFF'], decider_6)
        self.assertEqual(ACTIONS['PUMP_OUT'], decider_7)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick(self):
        """
        Testing the tick method in controller
        :return:
        """
        pump_address = Pump('127.0.0.1', 8080)
        sensor_address = Sensor('127.0.0.1', 8083)
        decider_vals = Decider(100, .10)
        controller_all = Controller(sensor_address, pump_address, decider_vals)
        sensor_address.measure = MagicMock(return_value=95)
        pump_address.get_state = MagicMock(return_value=pump_address.PUMP_IN)
        decider_vals.decide = MagicMock(return_value=pump_address.PUMP_IN)
        pump_address.set_state = MagicMock(return_value=True)
        controller_all.tick()
        sensor_address.measure.assert_called_with()
        pump_address.get_state.assert_called_with()
        decider_vals.decide.assert_called_with(
            95, pump_address.PUMP_IN, ACTIONS)
