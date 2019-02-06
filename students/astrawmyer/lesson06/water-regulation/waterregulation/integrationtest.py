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
        # Initialize controller, decider, pump, sensor.
        sensor = Sensor('127.0.0.1', 8000)
        pump = Pump('127.0.0.1', 8000)
        decider = Decider(50,5)
        controller = Controller(sensor, pump, decider)
        
        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=pump.PUMP_OFF)
        sensor.measure = MagicMock(return_value=25)

        
        self.assertEqual(Pump.PUMP_IN,controller.tick())

