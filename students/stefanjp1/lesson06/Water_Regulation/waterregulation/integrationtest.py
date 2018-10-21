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

        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

        self.sensor = Sensor('127.0.0.1', 8000)

        self.decider = Decider(100, .05)

        self.controller = Controller(self.sensor, self.pump, self.decider)

        self.test_output = []

    def test_integration(self):
        ''' Test the integration of all the components in the controller '''

        for pump_action in self.actions.values():
            for water_level in [90, 100, 110]:
                self.sensor.measure = MagicMock(return_value=water_level)
                self.pump.get_state = MagicMock(return_value=pump_action)
                self.test_output.append(self.controller.tick())

        self.assertEqual(self.test_output,
                         [True, True, True, True, True,
                          True, True, True, True])
