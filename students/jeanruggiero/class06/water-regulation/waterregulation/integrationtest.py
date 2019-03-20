"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from .controller import Controller
from .decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    pump = MagicMock()
    pump.get_state = MagicMock(return_value=1)
    pump.set_state = MagicMock(return_value=True)
    pump.PUMP_IN = 1
    sensor = MagicMock()
    sensor.measure = MagicMock(return_value=5)

    decider = Decider(10, 0.1)
    controller = Controller(sensor, pump, decider)

    def test_controller(self):
        """
        Integration test of Decider and Controller.
        """

        self.assertEqual(self.controller.tick(), True)
        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.pump.set_state.assert_called_with(1)
