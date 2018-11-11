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

    # write an integration test that combines controller and decider,
    #       using a MOCKED sensor and pump.

    def test_module(self):
        """
        test controller
        """
        decider = Decider(100, 0.1)
        pump = Pump('127.0.0', 9000)
        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=Pump.PUMP_OUT)
        sensor = Sensor('127.0.0', 8000)
        sensor.measure = MagicMock(return_value=80)

        controller = Controller(sensor, pump, decider)
        self.assertEqual(True, controller.tick())
