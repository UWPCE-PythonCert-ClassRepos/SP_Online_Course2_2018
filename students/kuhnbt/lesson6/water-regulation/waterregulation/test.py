"""
This module provides unit tests for the water regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """
    def test_decider(self):
        """Unit tests for decider"""
        decider = Decider(10, .1)
        actions = {
            'PUMP_IN': 1,
            'PUMP_OUT': 2,
            'PUMP_OFF': 3,
        }
        self.assertEqual(decider.decide(5, 'PUMP_IN', actions), 1)
        self.assertEqual(decider.decide(5, 'PUMP_OUT', actions), 3)
        self.assertEqual(decider.decide(5, 'PUMP_OFF', actions), 1)

        self.assertEqual(decider.decide(9.5, 'PUMP_IN', actions), 1)
        self.assertEqual(decider.decide(9.5, 'PUMP_OUT', actions), 3)
        self.assertEqual(decider.decide(9.5, 'PUMP_OFF', actions), 3)

        self.assertEqual(decider.decide(10.5, 'PUMP_IN', actions), 3)
        self.assertEqual(decider.decide(10.5, 'PUMP_OUT', actions), 2)
        self.assertEqual(decider.decide(10.5, 'PUMP_OFF', actions), 3)

        self.assertEqual(decider.decide(15, 'PUMP_IN', actions), 3)
        self.assertEqual(decider.decide(15, 'PUMP_OUT', actions), 2)
        self.assertEqual(decider.decide(15, 'PUMP_OFF', actions), 2)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        self.sensor = Sensor('http://localhost', '8080')
        self.pump = Pump('http://localhost', '8080')
        self.decider = Decider(10, .1)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.pump.set_state = MagicMock(return_value=True)
        self.decider.decide = MagicMock(return_value='PUMP_IN')

    def test_controller(self):
        """Test controller module"""
        self.sensor.measure = MagicMock(return_value=1)
        self.pump.get_state = MagicMock(return_value=1)
        self.pump.set_state = MagicMock(return_value=1)

        self.controller.tick()

        self.sensor.measure.assert_any_call()
        self.pump.get_state.assert_any_call()
        self.pump.set_state.assert_called_with('PUMP_IN')
