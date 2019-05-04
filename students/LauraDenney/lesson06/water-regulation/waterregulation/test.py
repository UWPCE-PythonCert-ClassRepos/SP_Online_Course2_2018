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
        self.decider = Decider(10, 0.05)
        self.pump = Pump('127.0.0.1', 8000)
        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }
        self.PUMP_IN = 1
        self.PUMP_OFF = 0
        self.PUMP_OUT = -1

    def test_off_low(self):
        '''test for off state, and lower water level'''
        value = self.decider.decide(8, "PUMP_OFF", self.actions)
        self.assertEqual(value, self.PUMP_IN)

    def test_off_high(self):
        '''test for off state, and high water level'''
        value = self.decider.decide(12, "PUMP_OFF", self.actions)
        self.assertEqual(value, self.PUMP_OUT)

    def test_off_middle(self):
        '''test for off state, and water level between margins'''
        value = self.decider.decide(10.2, "PUMP_OFF", self.actions)
        self.assertEqual(value, self.PUMP_OFF)

    def test_in_high(self):
        '''test for pump-in state, and high water level'''
        value = self.decider.decide(12, "PUMP_IN", self.actions)
        self.assertEqual(value, self.PUMP_OFF)

    def test_in_low(self):
        '''test for pump-in state, and low water level'''
        value = self.decider.decide(9, "PUMP_IN", self.actions)
        self.assertEqual(value, self.PUMP_IN)

    def test_out_low(self):
        '''test for pump-out state, and low water level'''
        value = self.decider.decide(9, "PUMP_OUT", self.actions)
        self.assertEqual(value, self.PUMP_OFF)

    def test_out_high(self):
        '''test for pump-out state, and high water level'''
        value = self.decider.decide(11, "PUMP_OUT", self.actions)
        self.assertEqual(value, self.PUMP_OUT)

    # def test_dummy(self):
    #     """
    #     Just some example syntax that you might use
    #     """

    #     pump = Pump('127.0.0.1', 8000)
    #     pump.set_state = MagicMock(return_value=True)

    #     self.fail("Remove this test.")


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        self.decider = Decider(10, 0.05)
        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1', 8000)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }
        self.PUMP_IN = 1
        self.PUMP_OFF = 0
        self.PUMP_OUT = -1

    def test_queries(self):
        '''test for controller module, to test it queries
            the other modules'''
        self.sensor.measure = MagicMock(return_value=8)
        self.pump.get_state = MagicMock(return_value="PUMP_OFF")
        self.pump.set_state = MagicMock(return_value=True)
        self.decider.decide = MagicMock(return_value="PUMP_IN")
        value = self.controller.tick()

        self.decider.decide.assert_called_with(8, "PUMP_OFF", self.actions)
        self.pump.set_state.assert_called_with("PUMP_IN")
        self.assertEqual(value, True)
