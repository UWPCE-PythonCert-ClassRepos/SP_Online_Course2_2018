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

    actions = {'PUMP_IN': 1, 'PUMP_OUT': -1, 'PUMP_OFF': 0}

    def test_pump_off_h_below_margin(self):
        """
        test PUMP_OFF + height below lower margin = PUMP_IN
        """
        decider = Decider(10, .1)
        action = decider.decide(8, self.actions['PUMP_OFF'], self.actions)
        self.assertEqual(self.actions['PUMP_IN'], action)

    def test_pump_off_h_at_low_margin(self):
        """
        test PUMP_OFF + height at lower margin = PUMP_OFF
        """
        decider = Decider(10, .1)
        action = decider.decide(9, self.actions['PUMP_OFF'], self.actions)
        self.assertEqual(self.actions['PUMP_OFF'], action)

    def test_pump_off_h_at_target(self):
        """
        test PUMP_OFF + height at target = PUMP_OFF
        """
        decider = Decider(10, .1)
        action = decider.decide(10, self.actions['PUMP_OFF'], self.actions)
        self.assertEqual(self.actions['PUMP_OFF'], action)

    def test_pump_off_h_at_high_margin(self):
        """
        test PUMP_OFF + height at upper margin = PUMP_OFF
        """
        decider = Decider(10, .1)
        action = decider.decide(11, self.actions['PUMP_OFF'], self.actions)
        self.assertEqual(self.actions['PUMP_OFF'], action)

    def test_pump_off_h_above_margin(self):
        """
        test PUMP_OFF + height above upper margin = PUMP_OUT
        """
        decider = Decider(10, .1)
        action = decider.decide(12, self.actions['PUMP_OFF'], self.actions)
        self.assertEqual(self.actions['PUMP_OUT'], action)

    def test_pump_in_h_below_target(self):
        """
        test PUMP_IN + height below target = PUMP_IN
        """
        decider = Decider(10, .1)
        action = decider.decide(9, self.actions['PUMP_IN'], self.actions)
        self.assertEqual(self.actions['PUMP_IN'], action)

    def test_pump_in_h_at_target(self):
        """
        test PUMP_IN + height at target = PUMP_IN
        """
        decider = Decider(10, .1)
        action = decider.decide(10, self.actions['PUMP_IN'], self.actions)
        self.assertEqual(self.actions['PUMP_IN'], action)

    def test_pump_in_h_above_target(self):
        """
        test PUMP_IN + height above target = PUMP_OFF
        """
        decider = Decider(10, .1)
        action = decider.decide(11, self.actions['PUMP_IN'], self.actions)
        self.assertEqual(self.actions['PUMP_OFF'], action)

    def test_pump_out_h_below_target(self):
        """
        test PUMP_OUT + height below target = PUMP_OFF
        """
        decider = Decider(10, .1)
        action = decider.decide(9, self.actions['PUMP_OUT'], self.actions)
        self.assertEqual(self.actions['PUMP_OFF'], action)

    def test_pump_out_h_at_target(self):
        """
        test PUMP_OUT + height below target = PUMP_OUT
        """
        decider = Decider(10, .1)
        action = decider.decide(10, self.actions['PUMP_OUT'], self.actions)
        self.assertEqual(self.actions['PUMP_OUT'], action)

    def test_pump_out_h_above_target(self):
        """
        test PUMP_OUT + height above target = PUMP_OUT
        """
        decider = Decider(10, .1)
        action = decider.decide(11, self.actions['PUMP_OUT'], self.actions)
        self.assertEqual(self.actions['PUMP_OUT'], action)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick_true(self):
        """
        Test that tick return True if pump.set_state returns True
        """
        sensor = Sensor('127.0.0.1', 8000)
        pump = Pump('127.0.0.1', 8000)
        decider = Decider(10, .1)
        controller = Controller(sensor, pump, decider)

        sensor.measure = MagicMock(return_value=10)
        pump.get_state = MagicMock(return_value=pump.PUMP_OFF)
        pump.set_state = MagicMock(return_value=True)

        self.assertTrue(controller.tick())

    def test_tick_false(self):
        """
        Test that tick return False if pump.set_state returns False
        """
        sensor = Sensor('127.0.0.1', 8000)
        pump = Pump('127.0.0.1', 8000)
        decider = Decider(10, .1)
        controller = Controller(sensor, pump, decider)

        sensor.measure = MagicMock(return_value=10)
        pump.get_state = MagicMock(return_value=pump.PUMP_OFF)
        pump.set_state = MagicMock(return_value=False)

        self.assertFalse(controller.tick())
