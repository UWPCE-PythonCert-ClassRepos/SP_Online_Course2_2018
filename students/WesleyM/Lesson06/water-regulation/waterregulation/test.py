"""Unit tests for the water-regulation module"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from controller import Controller
from decider import Decider

actions = {
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
        """
        deciders = Decider(100, .05)
        self.assertEqual(1, deciders.decide(90, actions['PUMP_OFF'], actions))
        self.assertEqual(1, deciders.decide(90, actions['PUMP_IN'], actions))
        self.assertEqual(-1, deciders.decide(120, actions['PUMP_OFF'], actions))
        self.assertEqual(-1, deciders.decide(120, actions['PUMP_OUT'], actions))
        self.assertEqual(0, deciders.decide(100, actions['PUMP_OFF'], actions))
        self.assertEqual(0, deciders.decide(120, actions['PUMP_IN'], actions))
        self.assertEqual(0, deciders.decide(90, actions['PUMP_OUT'], actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick(self):
        """
        Testing the tick method in controller
        """
        pump = Pump('127.0.0.1', 8000)
        sensor = Sensor('127.0.0.1', 8000)
        decider = Decider(100, .05)
        controller = Controller(sensor, pump, decider)
        sensor.measure = MagicMock(return_value=95)
        pump.get_state = MagicMock(return_value=pump.PUMP_IN)
        decider.decide = MagicMock(return_value=pump.PUMP_IN)
        pump.set_state = MagicMock(return_value=True)
        controller.tick()
        sensor.measure.assert_called_with()
        pump.get_state.assert_called_with()
        decider.decide.assert_called_with(95, pump.PUMP_IN, actions)
