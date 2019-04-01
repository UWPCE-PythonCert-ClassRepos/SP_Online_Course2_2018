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

    actions = {'PUMP_IN': 1, 'PUMP_OUT': -1, 'PUMP_OFF': 0}

    def test_system(self):
        """
        test controller and decider
        """
        sensor = Sensor('127.0.0.1', 8000)
        sensor.measure = MagicMock(return_value=10)

        pump = Pump('127.0.0.1', 8000)
        pump.get_state = MagicMock(return_value=pump.PUMP_OFF)
        pump.set_state = MagicMock(return_value=True)

        decider = Decider(10, .1)
        controller = Controller(sensor, pump, decider)

        # check that controller returning expected value
        self.assertTrue(controller.tick())

        # check that set_state getting correct input from decider
        pump.set_state.assert_called_with(self.actions['PUMP_OFF'])
