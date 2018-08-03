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

    def test_module(self):
        """
        Test the waterregulation module
        """

        sensor = Sensor('127.0.0.1', '3080')
        pump = Pump('127.0.0.1', '4080')
        decider = Decider(100, .10)

        controller = Controller(sensor, pump, decider)
        controller.pump.set_state = MagicMock(return_value=True)

        levels = range(89, 112)

        for action in controller.actions.values():
            for liquid_height in levels:
                controller.sensor.measure = MagicMock(return_value=liquid_height)
                controller.pump.get_state = MagicMock(
                    return_value=decider.decide(liquid_height, action, controller.actions)
                )
                controller.tick()
