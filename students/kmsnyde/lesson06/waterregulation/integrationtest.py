"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from controller import Controller
from decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    # provide decider and controller classes to use
    sensor = Sensor('127.0.0.1', '8000')
    pump = Pump('127.0.0.1', '8000')
    dec = Decider(100, .05)
    con = Controller(sensor, pump, dec)

    def test_int(self):
        """run an integration test"""

        # set MagicMock with True to test acknowledge reuest
        self.con.pump.set_state = MagicMock(return_value=True)
        self.con.pump.get_state = MagicMock(return_value="PUMP_IN")
        self.con.sensor.measure = MagicMock(return_value=100)
        self.con.tick()
        self.con.pump.get_state\
            = MagicMock(return_value=self.dec.decide(self.con.sensor.measure(),
                                                     self.con.pump.get_state(),
                                                     self.con.actions))
