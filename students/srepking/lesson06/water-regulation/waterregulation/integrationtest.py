"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from waterregulation.pump.pump import Pump
from waterregulation.sensor.sensor import Sensor
from waterregulation.controller import Controller
from waterregulation.decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """
    def setUp(self):
        self.sensor = Sensor('127.0.0.1', '8001')
        self.pump = Pump('127.0.0.1', '8000')
        self.decider = Decider(5, .05)
        self.new_controller = Controller(self.sensor, self.pump, self.decider)
        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

    def test_pump_out(self):
        """Given a high water level (7) and the pump is off (0),
        show that the controller starts PUMP_OUT (-1).
        """
        # Set Liquid Level to 7, above target height of 5
        self.sensor.measure = MagicMock(return_value=7)
        self.pump.get_state = MagicMock(return_value=0)  # PUMP_OFF
        self.pump.set_state = MagicMock(return_value=True)  # Assume connection
        # with PUMP is made
        self.new_controller.tick()  # update values of tick
        self.assertEqual(self.new_controller.control_decision, -1)

    def test_pump_in(self):
        """Given a high water level (7) and PUMP_IN (1) show that the
        controller turns off pump.
        """
        # Set Liquid Level to 7, above target height of 5
        self.sensor.measure = MagicMock(return_value=7)
        self.pump.get_state = MagicMock(return_value=1)  # PUMP_IN
        self.pump.set_state = MagicMock(return_value=True)  # Assume
        # connection with PUMP is made
        self.new_controller.tick()  # update values of tick
        self.assertEqual(self.new_controller.control_decision, 0)
