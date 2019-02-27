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
        # setup controller
        self.sensor = Sensor('127.0.0.1', 8000)
        self.pump = Pump('127.0.0.1', 8000)
        self.decider = Decider(target_height=100, margin=.1)

        self.controller = Controller(sensor=self.sensor,
                                     pump=self.pump,
                                     decider=self.decider)

    def test_controller_begins_filling_when_low_then_stops_when_full(self):
        """
        Integration test testing pump starting at 0 level and then increasing.
        Testing that decider gives right command and controller sends this to
        pump over time.  We simulate changes in volume by adjusting
        sensor mock
        """

        # set start
        current_height = 0
        pump_state = 'PUMP_OFF'

        self.controller.sensor.measure = MagicMock(return_value=current_height)
        self.controller.pump.get_state = MagicMock(return_value=pump_state)
        self.controller.pump.set_state = MagicMock(return_value=True)

        # test motor starts
        self.controller.tick()
        self.controller.pump.set_state.assert_called_with(state='PUMP_IN')

        # re-testing to ensure this still keeps PUMP_IN
        self.controller.tick()
        self.controller.pump.set_state.assert_called_with(state='PUMP_IN')

        # increase until in limit
        # test motor turns off
        # increase until over limit
        # test motor turns off
