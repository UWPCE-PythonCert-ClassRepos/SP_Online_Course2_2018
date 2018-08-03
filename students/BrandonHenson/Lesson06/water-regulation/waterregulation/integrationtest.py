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

    def test_app(self):
        """
        Testing the app
        :return:
        """
        pump_address = Pump('127.0.0.1', '8080')
        sensor_address = Sensor('127.0.0.1', '8083')
        decider_vals = Decider(100, .10)
        controller_all = Controller(sensor_address, pump_address, decider_vals)
        controller_all.pump.set_state = MagicMock(return_value=True)
        for action in controller_all.actions.values():
            for water_level in range(50, 150, 5):
                # level of water
                controller_all.sensor.measure = \
                    MagicMock(return_value=water_level)
                # state of the pump
                controller_all.pump.get_state = MagicMock(
                    return_value=decider_vals.decide(
                        water_level, action, controller_all.actions))
                # run tick
                controller_all.tick()
