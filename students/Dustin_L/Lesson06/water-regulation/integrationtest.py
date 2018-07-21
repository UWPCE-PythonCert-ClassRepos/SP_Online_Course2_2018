#!/usr/bin/env python3
"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from waterregulation.pump import Pump
from waterregulation.sensor import Sensor

from waterregulation.controller import Controller
from waterregulation.decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.addr = '127.0.0.1'
        self.port = 8000
        self.target = 100
        self.margin = 0.05
        self.lower_margin = self.target - (self.target * self.margin)
        self.upper_margin = self.target + (self.target * self.margin)
        self.actions = {
            'PUMP_IN':  Pump.PUMP_IN,
            'PUMP_OUT': Pump.PUMP_OUT,
            'PUMP_OFF': Pump.PUMP_OFF,
        }

    def setUp(self):
        self.pump = Pump(self.addr, self.port)
        self.sensor = Sensor(self.addr, self.port)
        self.decider = Decider(self.target, self.margin)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_waterregulation(self):
        """Test the waterregulation module"""
        self.controller.pump.set_state = MagicMock(return_value=True)

        test_levels = [90, 100, 110]

        for pump_action in self.controller.actions.values():
            self.controller.pump.get_state = MagicMock(return_value=pump_action)

            for level in test_levels:
                self.controller.sensor.measure = MagicMock(return_value=level)
                self.controller.pump.get_state = MagicMock(
                    return_value=self.decider.decide(level,
                                                     pump_action,
                                                     self.controller.actions))
                self.controller.tick()
