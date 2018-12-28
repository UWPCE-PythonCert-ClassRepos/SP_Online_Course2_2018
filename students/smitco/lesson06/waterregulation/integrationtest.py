"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from controller import Controller
from decider import Decider

from pump.pump import Pump
from sensor.sensor import Sensor


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def setUp(self):
        """Set up controller for test"""

        self.sensor = Sensor('127.0.0.1', 8000)
        self.pump = Pump('127.0.0.1', 8000)
        self.decider = Decider(10, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_controller(self):
        """test controller tick method"""

        self.sensor.measure = MagicMock(return_value=11.3)
        self.pump.get_state = MagicMock(return_value='PUMP_IN')
        self.pump.set_state = MagicMock(return_value=True)

        self.controller.tick()

        self.pump.set_state.assert_called_with('PUMP_OFF')
