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

    def setUp(self):
        """ set up class variables """
        self.actions = {'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1}

    def test_decider(self):
        """ test the decider class """
        decider = Decider(100, .05)
        self.assertEqual(-1, decider.decide(120, -1, self.actions))
        self.assertEqual(1, decider.decide(94, 0, self.actions))
        self.assertEqual(0, decider.decide(100, 0, self.actions))
        self.assertEqual(0, decider.decide(111, 1, self.actions))
        self.assertEqual(1, decider.decide(100, 1, self.actions))
        self.assertEqual(0, decider.decide(93, -1, self.actions))
        self.assertEqual(-1, decider.decide(110, 0, self.actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        """Set up for testing controller"""
        self.pump = Pump('127.0.0.1', 8001)
        self.pump.set_state = MagicMock(return_value=True)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OFF)
        self.sensor = Sensor('127.0.0.1', 8000)
        self.sensor.measure = MagicMock(return_value=100)
        self.decider = Decider(100, .05)
        self.decider.decide = MagicMock(return_value=self.pump.PUMP_OFF)

        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.controller.tick()

        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

    def test_controller(self):
        """
        Tests for controller and tick
        """
        self.pump.get_state.assert_called_with()
        self.assertEqual(0, self.pump.get_state())

        self.sensor.measure.assert_called_with()
        self.assertEqual(100, self.sensor.measure())

        self.decider.decide.assert_called_with(
            100, self.actions['PUMP_OFF'], self.actions
        )
        self.assertEqual(0, self.decider.decide(100, 0, self.actions))

        self.pump.set_state.assert_called_with(self.actions['PUMP_OFF'])
        self.assertEqual(True, self.pump.set_state(self.actions['PUMP_OFF']))
