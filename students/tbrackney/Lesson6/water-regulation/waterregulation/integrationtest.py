"""
Module tests for the water-regulation module
"""
# pylint: disable=duplicate-code

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
        """Create Dummy instance"""
        self.sensor = Sensor('127.0.0.1', '1111')
        self.pump = Pump('127.0.0.1', '2222')
        self.decider = Decider(100, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF
        }

    def test_module(self):
        """Basic integration test for waterregulation module"""
        cur_height = 50
        cur_act = self.actions['PUMP_OFF']
        self.sensor.measure = MagicMock(return_value=cur_height)
        self.pump.get_state = MagicMock(return_value=cur_act)
        self.pump.set_state = MagicMock(return_value=True)

        next_act = self.decider.decide(cur_height, cur_act, self.actions)
        self.assertEqual(next_act, self.actions['PUMP_IN'])
        success = self.controller.tick()
        self.assertEqual(True, success)
