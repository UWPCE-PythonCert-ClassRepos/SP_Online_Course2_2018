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
        self.pump = Pump('127.0.0.1', '8000')
        self.sensor = Sensor('127.0.0.2', '8001')
        self.decider = Decider(100, .05)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.controller.pump.set_state = MagicMock(return_value=True)

    def test_integration(self):
        """test for integration"""

        for action in self.controller.actions.values():
            for water_level in range(80, 150, 5):
                self.controller.sensor.measure = MagicMock(
                    return_value=water_level)

                self.controller.pump.get_state = MagicMock(
                    return_value=self.decider.decide(
                        water_level, action, self.controller.actions))

                self.controller.tick()
