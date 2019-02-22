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
    using a MOCKED sensor ad pump
    """

    def setUp(self):
        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1', 7000)
        self.decider = Decider(100, 0.5)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.controller.pump.set_state = MagicMock(return_value=True)
        self.actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1,
        }

    def test_integration(self):
        """
        Integration test for water regulation module
        """
        value_pump_get_state = self.actions['PUMP_OFF']
        self.pump.get_state = MagicMock(return_value=value_pump_get_state)

        sensor_measurement = 99.4
        self.sensor.measure = MagicMock(return_value=sensor_measurement)

        new_state = self.decider.decide(sensor_measurement,
                                        value_pump_get_state,
                                        self.actions)

        self.controller.tick()

        self.assertEqual(self.pump.set_state(new_state), True)
