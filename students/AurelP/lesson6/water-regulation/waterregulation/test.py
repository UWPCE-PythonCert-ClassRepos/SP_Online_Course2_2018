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
        """
        setup class
        """
        self.decider = Decider(300, 0.10)
        self.actions = {'PUMP_IN': 1, 'PUMP_OUT': -1, 'PUMP_OFF': 0, }

    def test_decide_off(self):
        """
        test for pump off
        """
        a = self.decider.decide(250, self.actions['PUMP_OFF'], self.actions)
        b = self.actions['PUMP_IN']
        self.assertEqual(a, b)
        a = self.decider.decide(310, self.actions['PUMP_OFF'], self.actions)
        b = self.actions['PUMP_OFF']
        self.assertEqual(a, b)
        a = self.decider.decide(300, self.actions['PUMP_OFF'], self.actions)
        b = self.actions['PUMP_OFF']
        self.assertEqual(a, b)

    def test_decide_in(self):
        """
        test for pump in
        """
        a = self.decider.decide(320, self.actions['PUMP_IN'], self.actions)
        b = self.actions['PUMP_OFF']
        self.assertEqual(a, b)
        a = self.decider.decide(250, self.actions['PUMP_IN'], self.actions)
        b = self.actions['PUMP_IN']
        self.assertEqual(a, b)

    def test_decide_out(self):
        """
        test for pump out
        """
        a = self.decider.decide(290, self.actions['PUMP_OUT'], self.actions)
        b = self.actions['PUMP_OFF']
        self.assertEqual(a, b)
        a = self.decider.decide(350, self.actions['PUMP_OUT'], self.actions)
        b = self.actions['PUMP_OUT']
        self.assertEqual(a, b)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        """
        Just some example syntax that you might use
        """
        self.pump = Pump('127.0.0.1', 1)
        self.sensor = Sensor('127.0.0.2', 2)
        self.decider = Decider(300, 0.10)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_tick(self):
        """
        test for controller
        """
        self.sensor.measure = MagicMock(return_value=200)
        self.pump.get_state = MagicMock(return_value=Pump.PUMP_OFF)
        self.pump.set_state = MagicMock(return_value=True)
        self.assertTrue(self.controller.tick())
        self.pump.set_state = MagicMock(return_value=False)
        self.assertFalse(self.controller.tick())
