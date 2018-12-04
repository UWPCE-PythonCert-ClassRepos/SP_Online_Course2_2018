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

    def intergrate_test(self):
        """
        Using Ghassan's code as an template
        """
        p = Pump('127.0.0.1', 8080)
        s = Sensor('127.0.0.1', 8083)
        d = Decider(100, .10)
        c = Controller(s, p, d)
        c.pump.set_state = MagicMock(return_value=True)
        for action in c.actions.values():
            for water_level in range(50, 150, 5):
                c.sensor.measure = MagicMock(return_value=water_level)
                c.pump.get_state = MagicMock(return_value=d.decide(water_level, action, c.actions))
                c.tick()
