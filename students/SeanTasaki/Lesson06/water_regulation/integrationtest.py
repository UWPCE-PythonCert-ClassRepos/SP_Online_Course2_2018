"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from waterregulation.pump import Pump
from waterregulation.sensor import Sensor

from waterregulation.controller import Controller
from waterregulation.decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def setUp(self):
        """Setup docstring."""
        self.address = "127.0.0.1"
        self.port = "8000"

    def test_integration(self):
        """Method docstring."""
        sensor = Sensor(self.address, self.port)
        pump = Pump(self.address, self.port)
        decider = Decider(100, .05)
        controller = Controller(sensor, pump, decider)
        for level in range(0, 200, 10):
            for action in controller.actions.values():
                sensor.measure = MagicMock(return_value=level)
                pump.get_state = MagicMock(return_value=action)
                pump.set_state = MagicMock(return_value=True)
                controller.tick()
        pump.set_state = MagicMock(return_value=False)
        controller.tick()
        