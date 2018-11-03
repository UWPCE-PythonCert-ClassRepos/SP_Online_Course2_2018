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
        """Integration test combining controller and decider."""

        d_i = Decider(100, 0.05)
        p_i = Pump('127.0.0.1', '8000')
        s_i = Sensor('127.0.0.2', '8000')
        c_i = Controller(s_i, p_i, d_i)
        c_i.pump.set_state = MagicMock(return_value=True)

        for water_level in range(75, 125, 5):
            for action in c_i.actions.values():
                # Measuring water level.
                c_i.sensor.measure = MagicMock(return_value=water_level)
                #  Checking pump state.
                c_i.pump.get_state = MagicMock(return_value=d_i.decide
                                               (water_level, action,
                                                c_i.actions))
                c_i.tick()
