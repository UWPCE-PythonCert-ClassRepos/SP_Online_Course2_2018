"""
Unit tests for the water-regulation module
"""
# pylint: disable=duplicate-code

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
        """Create dummy instance"""
        self.decider = Decider(100, 0.05)
        self.actions = {"PUMP_IN": 1, "PUMP_OUT": -1, "PUMP_OFF": 0}

    def test_under_margin(self):
        """below lower limit and pump off"""
        call = self.decider.decide(90, self.actions['PUMP_OFF'], self.actions)
        expected = self.actions['PUMP_IN']
        self.assertEqual(call, expected)

    def test_over_margin(self):
        """above upper limit and pump off"""
        call = self.decider.decide(110, self.actions['PUMP_OFF'], self.actions)
        expected = self.actions['PUMP_OUT']
        self.assertEqual(call, expected)

    def test_within_bounds1(self):
        """above target within margin and pump off"""
        call = self.decider.decide(102, self.actions['PUMP_OFF'], self.actions)
        expected = self.actions['PUMP_OFF']
        self.assertEqual(call, expected)

    def test_within_bounds2(self):
        """below target within margin and pump off"""
        call = self.decider.decide(98, self.actions['PUMP_OFF'], self.actions)
        expected = self.actions['PUMP_OFF']
        self.assertEqual(call, expected)

    def test_filled(self):
        """above target and pumping in"""
        call = self.decider.decide(110, self.actions['PUMP_IN'], self.actions)
        expected = self.actions['PUMP_OFF']
        self.assertEqual(call, expected)

    def test_filled2(self):
        """At target and pumping in"""
        call = self.decider.decide(100, self.actions['PUMP_IN'], self.actions)
        expected = self.actions['PUMP_OFF']
        self.assertEqual(call, expected)

    def test_not_filled(self):
        """Below Target and pumping in"""
        call = self.decider.decide(95, self.actions['PUMP_IN'], self.actions)
        expected = self.actions['PUMP_IN']
        self.assertEqual(call, expected)

    def test_drained(self):
        """Below target and pumping out"""
        call = self.decider.decide(98, self.actions['PUMP_OUT'], self.actions)
        expected = self.actions['PUMP_OFF']
        self.assertEqual(call, expected)

    def test_drained2(self):
        """At target and pumping out"""
        call = self.decider.decide(100, self.actions['PUMP_OUT'], self.actions)
        expected = self.actions['PUMP_OFF']
        self.assertEqual(call, expected)

    def test_draining(self):
        """Above target and pumping out"""
        call = self.decider.decide(105, self.actions['PUMP_OUT'], self.actions)
        expected = self.actions['PUMP_OUT']
        self.assertEqual(call, expected)

    def test_invalid_current_state(self):
        """Value outside of bounds"""
        with self.assertRaises(ValueError):
            self.decider.decide(105, 5, self.actions)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """
    def setUp(self):
        """Create dummy instance"""
        self.sensor = Sensor('127.0.0.1', 1111)
        self.pump = Pump('127.0.0.1', 2222)
        self.decider = Decider(100, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF
        }

    def test_tick(self):
        """Test behavior of tick method"""
        height = 50
        cur_act = self.actions['PUMP_OFF']
        next_act = self.actions['PUMP_IN']

        self.sensor.measure = MagicMock(return_value=height)
        self.pump.get_state = MagicMock(return_value=cur_act)
        self.decider.decide = MagicMock(return_value=next_act)
        self.pump.set_state = MagicMock(return_value=True)

        success = self.controller.tick()
        self.assertEqual(True, success)

        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.decider.decide.assert_called_with(height, cur_act, self.actions)
        self.pump.set_state.assert_called_with(next_act)

    def test_fail(self):
        """Test for exception in controller.tick method"""
        height = 50
        cur_act = self.actions['PUMP_OFF']
        next_act = self.actions['PUMP_IN']

        self.sensor.measure = MagicMock(return_value=height)
        self.pump.get_state = MagicMock(return_value=cur_act)
        self.decider.decide = MagicMock(return_value=next_act)
        self.pump.set_state = MagicMock(return_value=False)

        success = self.controller.tick()
        self.assertEqual(False, success)
