"""
Module tests for the water-regulation module
"""
import unittest
from unittest.mock import MagicMock
from pump.pump import Pump
from sensor.sensor import Sensor
from .decider import Decider
from .controller import Controller


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def setUp(self):
        self.sensor = Sensor('127.0.0.1', '168')
        self.pump = Pump('127.0.0.1', '168')
        self.decider = Decider(10, 0.5)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_module(self):
        """
        Testing module
        """
        test_range = [i * 0.25 for i in range(0, 49)]
        for j in self.controller.actions.values():
            for k in test_range:
                self.controller.sensor.measure = MagicMock(return_value=k)
                self.controller.pump.get_state = MagicMock(return_value=j)
                self.controller.decider.decide = MagicMock(return_value=j)
                self.controller.pump.set_state = MagicMock(return_value=j)
                self.controller.tick()
