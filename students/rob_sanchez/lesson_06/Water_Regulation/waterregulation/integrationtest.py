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

    def test_module_integration(self):
        """
            integration test that combines controller and
            decider using a MOCKED sensor and pump
        """
        sensor_values = [89, 90, 100, 110, 111]
        pump_off_results = []
        pump_in_results = []
        pump_out_results = []

        # Test PUMP_OFF actions
        #######################
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OFF)

        pump_off_expected = [self.pump.PUMP_IN,
                             self.pump.PUMP_OFF,
                             self.pump.PUMP_OFF,
                             self.pump.PUMP_OFF,
                             self.pump.PUMP_OUT]
        for val in sensor_values:
            self.sensor.measure = MagicMock(return_value=val)
            self.controller.tick()
            result = self.decider.decide(self.sensor.measure(),
                                         self.pump.get_state(),
                                         self.actions)
            pump_off_results.append(result)

        self.assertEqual(pump_off_results, pump_off_expected)

        # Test PUMP_IN actions
        ######################
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_IN)

        pump_in_expected = [self.pump.PUMP_IN,
                            self.pump.PUMP_IN,
                            self.pump.PUMP_IN,
                            self.pump.PUMP_OFF,
                            self.pump.PUMP_OFF]
        for val in sensor_values:
            self.sensor.measure = MagicMock(return_value=val)
            self.controller.tick()
            result = self.decider.decide(self.sensor.measure(),
                                         self.pump.get_state(),
                                         self.actions)
            pump_in_results.append(result)

        self.assertEqual(pump_in_results, pump_in_expected)

        # Test PUMP_OUT actions
        #######################
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OUT)

        pump_out_expected = [self.pump.PUMP_OFF,
                             self.pump.PUMP_OFF,
                             self.pump.PUMP_OUT,
                             self.pump.PUMP_OUT,
                             self.pump.PUMP_OUT]
        for val in sensor_values:
            self.sensor.measure = MagicMock(return_value=val)
            self.controller.tick()
            result = self.decider.decide(self.sensor.measure(),
                                         self.pump.get_state(),
                                         self.actions)
            pump_out_results.append(result)

        self.assertEqual(pump_out_results, pump_out_expected)
