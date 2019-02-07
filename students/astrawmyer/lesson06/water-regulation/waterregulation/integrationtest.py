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
    def test_modules(self):
        """
        Tests that all modules are called correctly
        """

        # Initialize controller, decider, pump, sensor.
        sensor = Sensor('127.0.0.1', 9000)
        pump = Pump('127.0.0.1', 9000)
        decider = Decider(50, 10)
        controller = Controller(sensor, pump, decider)

        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=pump.PUMP_IN)
        sensor.measure = MagicMock(return_value=65)

        self.assertEqual(Pump.PUMP_IN, controller.tick())
