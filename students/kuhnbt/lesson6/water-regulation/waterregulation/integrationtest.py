"""
The water-regulation module integration tests
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
        """Integration test for module"""
        self.pump = Pump('128.0.0.1', '8080')
        self.sensor = Sensor('128.0.0.1', '8080')
        self.decider = Decider(10, .2)
        self.controller = Controller(self.sensor, self.pump, self.decider)

        self.sensor.measure = MagicMock(return_value=6)
        self.pump.get_state = MagicMock(return_value='PUMP_OUT')
        self.pump.set_state = MagicMock(return_value=1)

        status = self.controller.tick()
        self.assertEqual(status, 1)
        self.pump.set_state.assert_called_with(0)
