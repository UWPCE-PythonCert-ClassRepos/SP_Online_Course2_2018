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

    @classmethod
    def setUpClass(cls):
        cls.decider = Decider(5, 0.1)
        cls.actions = {
            'PUMP_IN': 'pump_in',
            'PUMP_OFF': 'pump_off',
            'PUMP_OUT': 'pump_out'
        }

    def test_pump_off(self):
        """Tests behavior when the pump is off"""
        self.assertEqual(
            self.decider.decide(5, 'PUMP_OFF', self.actions), 'pump_off')
        self.assertEqual(
            self.decider.decide(5.5, 'PUMP_OFF', self.actions), 'pump_off')
        self.assertEqual(
            self.decider.decide(4.5, 'PUMP_OFF', self.actions), 'pump_off')
        self.assertEqual(
            self.decider.decide(5.6, 'PUMP_IN', self.actions), 'pump_off')
        self.assertEqual(
            self.decider.decide(4.4, 'PUMP_OUT', self.actions), 'pump_off')

    def test_pump_in(self):
        """Tests behavior when the pump is pumping in"""
        self.assertEqual(
            self.decider.decide(4.4, 'PUMP_OFF', self.actions), 'pump_in')
        self.assertEqual(
            self.decider.decide(4.9, 'PUMP_IN', self.actions), 'pump_in')

    def test_pump_out(self):
        """Tests behavior when the pump is pumping out"""
        self.assertEqual(
            self.decider.decide(5.6, 'PUMP_OFF', self.actions), 'pump_out')
        self.assertEqual(
            self.decider.decide(5.1, 'PUMP_OUT', self.actions), 'pump_out')


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick(self):
        """Tests the tick"""
        # Create a controller, and all the things it needs
        pump = Pump('127.0.0.1', 8000)
        sensor = Sensor('127.0.0.1', 8000)
        decider = Decider(5, 5)
        controller = Controller(sensor, pump, decider)

        # Now mock a few items
        pump.get_state = MagicMock(return_value=Pump.PUMP_OFF)
        sensor.measure = MagicMock(return_value=5)
        decider.decide = MagicMock(return_value=True)

        # Testing if true/normal
        pump.set_state = MagicMock(return_value=True)
        self.assertEqual(controller.tick(), True)

        # Testing if false/abnormal
        pump.set_state = MagicMock(return_value=False)
        self.assertEqual(controller.tick(), False)
