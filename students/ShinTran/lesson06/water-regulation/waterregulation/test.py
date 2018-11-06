"""
Unit tests for the water-regulation module
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

    def test_decider(self):
        """Tests for each of the behaviors defined for Decider.decide"""

        decider = Decider(100, 0.05)

        self.assertEqual(decider.decide(85, 0, ACTIONS), 1)
        self.assertEqual(decider.decide(107, 0, ACTIONS), -1)
        self.assertEqual(decider.decide(96, 0, ACTIONS), 0)

        self.assertEqual(decider.decide(101, 1, ACTIONS), 0)
        self.assertEqual(decider.decide(75, 1, ACTIONS), 1)

        self.assertEqual(decider.decide(80, -1, ACTIONS), 0)
        self.assertEqual(decider.decide(103, -1, ACTIONS), -1)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_controller(self):
        """Tests for each of the behaviors defined for Controller.tick"""
        sensor = Sensor('127.0.0.1', 8000)
        pump = Pump('127.0.0.1', 8000)
        decider = Decider(100, 0.05)
        controller = Controller(sensor, pump, decider)

        sensor.measure = MagicMock(return_value=95)
        pump.get_state = MagicMock(return_value=pump.PUMP_IN)
        decider.decide = MagicMock(return_value=pump.PUMP_IN)
        pump.set_state = MagicMock(return_value=True)

        controller.tick()
        sensor.measure.assert_called_with()
        pump.get_state.assert_called_with()
        decider.decide.assert_called_with(95, pump.PUMP_IN, ACTIONS)
