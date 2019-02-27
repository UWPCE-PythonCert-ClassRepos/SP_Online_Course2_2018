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
        """setup to use in integration testing"""
        self.sensor = Sensor('127.0.0.1', '8000')
        self.pump = Pump('127.0.0.1', '8001')
        self.decider = Decider(30, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.pump.set_state = MagicMock(return_value=True)

    def test_controller_decider(self):
        """
        test water-regulation module as a whole
        """
        for height in range(20, 40, 5):
            for state in self.controller.actions.values():
                for n_state in self.controller.actions.values():
                    self.pump.get_state = MagicMock(return_value=state)
                    self.sensor.measure = MagicMock(return_value=height)
                    self.decider.decide = MagicMock(return_value=n_state)
                    self.controller.tick()
