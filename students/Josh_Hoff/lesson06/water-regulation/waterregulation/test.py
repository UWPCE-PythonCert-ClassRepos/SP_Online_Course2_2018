"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider

actions = {'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1}


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """
    def test_decider(self):

        decider = Decider(80, .05)

        for x in range(1, 76):
            self.assertEqual(decider.decide(x, 0, actions), 1)
        for x in range(76, 85):
            self.assertEqual(decider.decide(x, 0, actions), 0)
        for x in range(85, 120):
            self.assertEqual(decider.decide(x, 0, actions), -1)

        for x in range(81, 120):
            self.assertEqual(decider.decide(x, 1, actions), 0)
        for x in range(1, 76):
            self.assertEqual(decider.decide(x, 1, actions), 1)

        for x in range(1, 76):
            self.assertEqual(decider.decide(x, -1, actions), 0)
        for x in range(85, 120):
            self.assertEqual(decider.decide(x, -1, actions), -1)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """
    def test_controller(self):

        pump = Pump('0.0.0.1', 541)
        sensor = Sensor('0.0.0.1', 541)
        decider = Decider(80, .05)
        controller = Controller(sensor, pump, decider)

        sensor.measure = MagicMock(return_value=60)
        pump.get_state = MagicMock(return_value=1)
        decider.decide = MagicMock(return_value=-1)
        pump.set_state = MagicMock(return_value=True)

        controller.tick()
        sensor.measure.assert_called_with()
        pump.get_state.assert_called_with()
        decider.decide.assert_called_with(60, 1, actions)
