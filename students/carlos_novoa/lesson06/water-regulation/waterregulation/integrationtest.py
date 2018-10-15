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

    def setUp(self):
        self.sensor = Sensor('127.0.0.1', 8000)
        self.pump = Pump('127.0.0.1', 8000)
        self.pump.set_state = MagicMock(return_value=True)
        self.decider = Decider(50, .05)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

    def test_module(self):
        """ test that combines controller and decider """

        # measure
        self.controller.sensor.measure = MagicMock(return_value=47)

        # set state
        self.controller.pump.get_state = MagicMock(
            return_value=self.pump.PUMP_OFF)

        # decide
        level_cases = [47, 50, 53]
        for level in level_cases:
            for key in self.actions:
                print(key)
                self.controller.decider.decide(
                    level,
                    self.controller.pump.get_state,
                    self.actions)

        # set state
        self.assertEqual(True, self.controller.tick())
