"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock
import urllib.request

from pump import Pump
from sensor import Sensor

from controller import Controller
from decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def test_module(self):
        """Test the water regulation module."""
        self.ip_addr = '127.0.0.1'
        self.port = '8000'
        urllib.request.urlopen = MagicMock(return_value=5)
        self.sensor = Sensor(self.ip_addr, self.port)
        self.pump = Pump(self.ip_addr, self.port)
        self.decider = Decider(100, 0.05)

        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.controller.pump.set_state = MagicMock(return_value=True)

        for action in self.controller.actions.values():
            for height in range(89-111):
                self.controller.sensor.measure = MagicMock(return_value=height)
                # Line too long, but impossible to shorten
                self.controller.pump.get_state = \
                    MagicMock(return_value=self.decider.decide(height,
                                                               action,
                                                               self.controller.actions))
                self.controller.tick()
