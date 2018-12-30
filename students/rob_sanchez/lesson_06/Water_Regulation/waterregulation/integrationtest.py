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

        self.sensor = Sensor('127.0.0.1', 8000)

        self.decider = Decider(100, .10)

        self.controller = Controller(self.sensor, self.pump, self.decider)

        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

    def test_module(self):
        """
            integration test that combines controller and
            decider using a MOCKED sensor and pump
        """

        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OFF)
        self.sensor.measure = MagicMock(return_value=89)
        self.controller.tick()

        result = self.decider.decide(self.sensor.measure(),
                                     self.pump.get_state(),
                                     self.actions)

        self.assertEqual(result, self.actions['PUMP_IN'])
