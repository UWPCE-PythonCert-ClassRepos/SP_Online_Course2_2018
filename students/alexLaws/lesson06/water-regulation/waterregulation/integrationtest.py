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
        self.pump = Pump('127.0.0.1', 8000)
        self.pump.set_state = MagicMock(return_value=True)

        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

        self.sensor = Sensor('127.0.0.1', 8000)

        self.decider = Decider(100, .02)

        self.controller = Controller(self.sensor, self.pump, self.decider)

        self.output = []

    def test_module(self):
        """
        Test that the full waterregulation module works together correctly
        """

        for water_level in [90, 100, 110]:
            for pump_state in [self.pump.PUMP_IN,
                               self.pump.PUMP_OFF,
                               self.pump.PUMP_OUT]:
                self.pump.get_state = MagicMock(return_value=pump_state)
                self.sensor.measure = MagicMock(return_value=water_level)
                self.controller.tick()
                self.output.append(self.decider.decide(water_level,
                                                       pump_state,
                                                       self.actions))

        predicted = [self.pump.PUMP_IN,
                     self.pump.PUMP_IN,
                     self.pump.PUMP_OFF,
                     self.pump.PUMP_IN,
                     self.pump.PUMP_OFF,
                     self.pump.PUMP_OUT,
                     self.pump.PUMP_OFF,
                     self.pump.PUMP_OUT,
                     self.pump.PUMP_OUT]

        self.assertEqual(self.output, predicted)
