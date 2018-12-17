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
    'PUMP_IN': Pump.PUMP_IN,
    'PUMP_OUT': Pump.PUMP_OUT,
    'PUMP_OFF': Pump.PUMP_OFF
}


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def test_decider(self):
        """
        Test for the Decider class
        """

        decider = Decider(100, 0.1)

        self.assertEqual(decider.decide(
            80, Pump.PUMP_OFF, ACTIONS), ACTIONS['PUMP_IN'])
        self.assertEqual(decider.decide(
            120, Pump.PUMP_OFF, ACTIONS), ACTIONS['PUMP_OUT'])
        self.assertEqual(decider.decide(
            100, Pump.PUMP_OFF, ACTIONS), ACTIONS['PUMP_OFF'])
        self.assertEqual(decider.decide(
            80, Pump.PUMP_IN, ACTIONS), ACTIONS['PUMP_IN'])
        self.assertEqual(decider.decide(
            120, Pump.PUMP_IN, ACTIONS), ACTIONS['PUMP_OFF'])
        self.assertEqual(decider.decide(
            100, Pump.PUMP_IN, ACTIONS), ACTIONS['PUMP_IN'])
        self.assertEqual(decider.decide(
            80, Pump.PUMP_OUT, ACTIONS), ACTIONS['PUMP_OFF'])
        self.assertEqual(decider.decide(
            120, Pump.PUMP_OUT, ACTIONS), ACTIONS['PUMP_OUT'])
        self.assertEqual(decider.decide(
            100, Pump.PUMP_OUT, ACTIONS), ACTIONS['PUMP_OUT'])


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        """
        setUp method for Controller tests
        """

        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1', 8000)
        self.decider = Decider(100, 0.05)
        self.controller = Controller(
            self.sensor, self.pump, self.decider)

    def test_tick(self):
        """
        Test for the tick function
        """

        self.sensor.measure = MagicMock(return_value=90)
        self.pump.get_state = MagicMock(return_value=Pump.PUMP_OFF)
        self.decider.decide = MagicMock(return_value=Pump.PUMP_IN)
        self.pump.set_state = MagicMock(return_value=True)
        self.controller.tick()
        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.decider.decide.assert_called_with(
            90, self.pump.PUMP_OFF, self.controller.actions)
        self.pump.set_state.assert_called_with(self.pump.PUMP_IN)
