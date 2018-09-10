#integrationtest.py
#Natalie Rodriguez
#Lesson 6: Water Regulation

"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from controller import Controller
from decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    # TODO: write an integration test that combines controller and decider,
    #       using a MOCKED sensor and pump.

    def test_water(self):
        """
        the test method
        """
        pump = Pump('127.0.0.1', '8000')
        decider = Decider(100, 2)
        sensor = Sensor('127.0.0.1', '8000')
        controller = Controller(sensor, pump, decider)
        controller.pump.set_state = MagicMock(return_value=True)
        controller.pump.get_state = MagicMock(return_value=True)
        # level = [100, 100, 95]
        for act in controller.actions.values():
            for level in range(0, 200, 1):
                controller.sensor.measure = MagicMock(return_value=level)
                controller.pump.get_state = MagicMock(return_value=decider.decide(level, act, controller.actions))
                controller.pump.set_state = MagicMock(return_value=True)
                controller.tick()