"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def setUp(self):

        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)

        self.actions = {
            'PUMP_IN': pump.PUMP_IN,
            'PUMP_OUT': pump.PUMP_OUT,
            'PUMP_OFF': pump.PUMP_OFF,
        }

    def test_decider(self):
        """
        Test that the decider function correctly assigns the next state
        """

        decider = Decider(100, .05)

        off_to_in = decider.decide(90, self.actions['PUMP_OFF'],
                                   self.actions)
        self.assertEqual(off_to_in, self.actions['PUMP_IN'])

        off_to_out = decider.decide(110, self.actions['PUMP_OFF'],
                                    self.actions)
        self.assertEqual(off_to_out, self.actions['PUMP_OUT'])

        off_to_off_within_bounds = decider.decide(102,
                                                  self.actions['PUMP_OFF'],
                                                  self.actions)
        self.assertEqual(off_to_off_within_bounds, self.actions['PUMP_OFF'])

        off_to_off_lower_bound = decider.decide(95, self.actions['PUMP_OFF'],
                                                self.actions)
        self.assertEqual(off_to_off_lower_bound, self.actions['PUMP_OFF'])

        off_to_off_upper_bound = decider.decide(105, self.actions['PUMP_OFF'],
                                                self.actions)
        self.assertEqual(off_to_off_upper_bound, self.actions['PUMP_OFF'])

        in_to_off = decider.decide(101, self.actions['PUMP_IN'],
                                   self.actions)
        self.assertEqual(in_to_off, self.actions['PUMP_OFF'])

        in_to_in = decider.decide(85, self.actions['PUMP_IN'],
                                  self.actions)
        self.assertEqual(in_to_in, self.actions['PUMP_IN'])

        out_to_off = decider.decide(99, self.actions['PUMP_OUT'],
                                    self.actions)
        self.assertEqual(out_to_off, self.actions['PUMP_OFF'])

        out_to_out = decider.decide(102, self.actions['PUMP_OUT'],
                                    self.actions)
        self.assertEqual(out_to_out, self.actions['PUMP_OUT'])


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):

        self.pump = Pump('127.0.0.1', 8000)
        self.pump.set_state = MagicMock(return_value=True)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_IN)

        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

        self.sensor = Sensor('127.0.0.1', 8000)
        self.sensor.measure = MagicMock(return_value=95)

        self.decider = Decider(100, .05)
        self.decider.decide = MagicMock(return_value=self.pump.PUMP_IN)

        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_controller(self):
        ''' Test the controller functionality '''

        self.assertEqual(self.controller.tick(), True)
        too_long = self.pump.PUMP_IN
        self.decider.decide.assert_called_with(current_height=95,
                                               current_action=too_long,
                                               actions=self.actions)
