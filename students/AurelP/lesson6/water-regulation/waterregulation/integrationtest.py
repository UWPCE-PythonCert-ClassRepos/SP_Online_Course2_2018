"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def setUp(self):
        """
        This method does a setup for integration testing raterregulation
        """
        self.pump = Pump('127.0.0.1', 1000)
        self.sensor = Sensor('127.0.0.2', 2000)
        self.decider = Decider(300, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_tick(self):
        """
        This method performs an integration test for tick
        """
        self.sensor.measure = MagicMock(return_value=275)
        self.pump.get_state = MagicMock(return_value='PUMP_OFF')
        self.controller.tick = MagicMock(return_value='PUMP_OUT')
        self.assertEqual(self.controller.tick(), 'PUMP_OUT')
