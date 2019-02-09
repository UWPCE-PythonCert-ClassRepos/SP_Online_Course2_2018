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

    # TODO: write an integration test that combines controller and decider,
    #       using a MOCKED sensor and pump.
    def test_module(self):
        decider = Decider(100, 0.10)
        sensor = Sensor('127.0.0.1', '8000')
        sensor.measure = MagicMock(return_value=105)
        pump = Pump('127.0.0.1', '8000')

        controller = Controller(sensor,pump,decider)
        controller.pump.set_state=MagicMock(return_value = True)

        water_level = [89,100,111]

        for action in controller.actions.values():
            for levels in water_level:
                controller.sensor.measure = MagicMock(return_value= levels)
                controller.pump.get_state = MagicMock(return_value=decider.decide(levels, action, controller.actions))
                controller.tick()
