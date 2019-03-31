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

    def test_controller_decider(self):
        """
        Integration test for water-regulation controller controller
        """
        pump = Pump('127.0.0.1', 8000)

        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=Pump.PUMP_OUT)

        sensor = Sensor('127.0.0.1', 8000)

        sensor.measure = MagicMock(return_value=1.0)

        decider = Decider(1000.0, 0.5)

        controller = Controller(sensor, pump, decider)

        self.assertTrue(controller.tick())
