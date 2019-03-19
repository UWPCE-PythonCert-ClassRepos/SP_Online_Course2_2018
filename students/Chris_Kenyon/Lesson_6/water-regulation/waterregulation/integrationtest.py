"""
Module tests for the water-regulation program
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests
    """

    def test_module(self):
        """
        Function to test water regulation module
        """
        pump_loc = Pump('127.0.0.1', '8080')
        sensor_loc = Sensor('127.0.0.1', '8083')
        decider = Decider(100, .10)
        controller = Controller(sensor_loc, pump_loc, decider)
        controller.pump.set_state = MagicMock(return_value=True)
        for action in controller.actions.values():
            for water_level in range(50, 150, 5):
                controller.sensor.measure = MagicMock(
                    return_value=water_level)
                controller.pump.get_state = MagicMock(
                    return_value=decider.decide(
                        water_level, action, controller.actions))
                controller.tick()
