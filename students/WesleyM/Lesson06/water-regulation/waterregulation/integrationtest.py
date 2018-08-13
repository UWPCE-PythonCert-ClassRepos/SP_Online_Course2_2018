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

    def test_app(self):
        """Testing the Water Regulation Controller and Decider"""
        pump = Pump('127.0.0.1', '8000')
        sensor = Sensor('127.0.0.1', '8000')
        decider = Decider(100, .05)
        controller = Controller(sensor, pump, decider)
        controller.pump.set_state = MagicMock(return_value=True)
        for action in controller.actions.values():
            for water_level in range(50, 150, 5):
                # measuring the water level
                controller.sensor.measure = MagicMock(return_value=water_level)
                # getting the state of the pump
                controller.pump.get_state = MagicMock(return_value=decider.decide(\
                    water_level, action, controller.actions))
                # running the tick functions
                controller.tick()
