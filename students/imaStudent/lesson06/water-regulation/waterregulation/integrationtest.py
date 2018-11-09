"""
Integration tests for the water-regulation module
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

    def test_module(self):
        """
        Tests for the water-regulation module
        """
        sensor = Sensor("127.0.0.1", "5150")
        pump = Pump("127.0.0.1", "5051")
        decider = Decider(500, .05)
        controller = Controller(sensor, pump, decider)

        pump.set_state = MagicMock(return_value=True)

        for action in controller.actions:
            for level in range(0, 600, 50):
                sensor.measure = MagicMock(return_value=level)
                pump.get_state = MagicMock(return_value=action)
                next_pump_state = decider.decide(level, action,
                                                 controller.actions)

                controller.tick()
                pump.set_state.assert_called_with(next_pump_state)
