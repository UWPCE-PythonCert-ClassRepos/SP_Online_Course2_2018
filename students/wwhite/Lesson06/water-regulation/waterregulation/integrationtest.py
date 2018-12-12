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

    def test_integration(self):
        """
        Integration test that combines controller and decider
        using a MOCKED sensor and pump
        """

        pump = Pump('127.0.0.1', '8000')
        sensor = Sensor('127.0.0.1', '8000')
        decider = Decider(100, 0.05)
        controller = Controller(sensor, pump, decider)
        controller.pump.set_state = MagicMock(return_value=True)
        for action in controller.actions.values():
            for level in range(50, 150, 5):
                controller.sensor.measure = MagicMock(
                    return_value=level)
                controller.pump.get_state = MagicMock(
                    return_value=decider.decide(
                        level, action, controller.actions))
                controller.tick()
