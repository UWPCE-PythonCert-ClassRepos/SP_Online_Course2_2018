"""
AUTHOR: Micah Braun
PROJECT NAME: integrationtest.py (for waterregulation modules)
DATE CREATED: 10/19/2018
LAST-UPDATED: 10/29/2018
PURPOSE: Lesson 6
DESCRIPTION: Integration test combining both Controller
and Decider class functions to test for proper behavior.
"""
import unittest
from unittest.mock import MagicMock
from pump.pump import Pump
from sensor.sensor import Sensor
from waterregulation.controller import Controller
from waterregulation.decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    # noinspection PyMethodMayBeStatic
    def test_all(self):
        """
        Run full test on all components of waterregulation
        """
        pump_address = Pump('127.0.0.1', '2048')
        sensor_address = Sensor('127.0.0.1', '2048')
        decider_margins = Decider(100, .10)
        controller_all = Controller(sensor_address, pump_address,
                                    decider_margins)
        controller_all.pump.set_state = MagicMock(return_value=True)
        for action in controller_all.actions.values():
            for water_level in range(25, 150, 100):
                # water level (mocked)
                controller_all.sensor.measure = \
                    MagicMock(return_value=water_level)
                # pump state (mocked)
                controller_all.pump.get_state = MagicMock(
                    return_value=decider_margins.decide(
                        water_level, action, controller_all.actions))
                controller_all.tick()


if __name__ == '__main__':
    unittest.main()
