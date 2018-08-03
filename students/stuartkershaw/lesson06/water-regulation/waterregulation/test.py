"""
Unit tests for the water-regulation module
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

    def test_decider_decide(self):
        """
        Test the decide method
        """

        actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1
        }

        decider = Decider(100, .10)

        self.assertEqual(1, decider.decide(89, 0, actions))
        self.assertEqual(-1, decider.decide(111, 0, actions))
        self.assertEqual(0, decider.decide(95, 0, actions))
        self.assertEqual(0, decider.decide(101, 1, actions))
        self.assertEqual(1, decider.decide(99, 1, actions))
        self.assertEqual(0, decider.decide(99, -1, actions))
        self.assertEqual(-1, decider.decide(101, -1, actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_controller_tick(self):
        """
        Test the tick method
        """

        sensor = Sensor('127.0.0.1', '3080')
        pump = Pump('127.0.0.1', '4080')
        decider = Decider(100, .10)

        controller = Controller(sensor, pump, decider)

        sensor.measure = MagicMock(return_value=105)
        pump.get_state = MagicMock(return_value=pump.PUMP_IN)
        decider.decide = MagicMock(return_value=pump.PUMP_OFF)
        pump.set_state = MagicMock(return_value=True)

        controller.tick()

        sensor.measure.assert_called_with()
        pump.get_state.assert_called_with()
        decider.decide.assert_called_with(105, pump.PUMP_IN, controller.actions)
        pump.set_state.assert_called_with(pump.PUMP_OFF)
