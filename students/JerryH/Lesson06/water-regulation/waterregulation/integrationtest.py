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
        # write an integration test that combines controller and decider,
        #       using a MOCKED sensor and pump.
        pump_address = Pump('125.0.0.1', '8000')
        sensor_address = Sensor('125.0.0.2', '8000')
        decider = Decider(100, .1)
        controller = Controller(sensor_address, pump_address, decider)
        controller.pump.set_state = MagicMock(return_value=True)

        for action in controller.actions.values():
            for water_level in range(80, 120, 5):
                controller.sensor.measure = MagicMock(return_value=water_level)

                controller.pump.get_state = MagicMock(
                    return_value=decider.decide(
                        water_level, action, controller.actions))

                controller.tick()
