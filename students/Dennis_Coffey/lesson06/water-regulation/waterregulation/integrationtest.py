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
        """
        Sets up pump, sensor, decider and controller for use with
        unit tests.
        """

        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1', 8000)
        self.decider = Decider(target_height=100, margin=0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.pump.set_state = MagicMock(return_value=True)

    def test_waterregulation(self):
        """
        Random integration tests for water-regulation module
        """
        # Test with height of 125 and pump off
        self.sensor.measure = MagicMock(return_value=125)
        self.pump.get_state = MagicMock(return_value='PUMP_OFF')
        self.controller.tick()
        self.pump.set_state.assert_called_with(self.controller.
                                               actions['PUMP_OUT'])

        # Test with height of 125 and pump in
        self.sensor.measure = MagicMock(return_value=125)
        self.pump.get_state = MagicMock(return_value='PUMP_IN')
        self.controller.tick()
        self.pump.set_state.assert_called_with(self.controller.
                                               actions['PUMP_OFF'])

        # Test with height of 75 and pump off
        self.sensor.measure = MagicMock(return_value=75)
        self.pump.get_state = MagicMock(return_value='PUMP_OFF')
        self.controller.tick()
        self.pump.set_state.assert_called_with(self.controller.
                                               actions['PUMP_IN'])

        # Test with height of 75 and pump out
        self.sensor.measure = MagicMock(return_value=75)
        self.pump.get_state = MagicMock(return_value='PUMP_OUT')
        self.controller.tick()
        self.pump.set_state.assert_called_with(self.controller.
                                               actions['PUMP_OFF'])
