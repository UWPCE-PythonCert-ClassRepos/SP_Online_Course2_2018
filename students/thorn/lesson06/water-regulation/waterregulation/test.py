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

    Pump State Values:
        PUMP_IN  =  1
        PUMP_OFF =  0
        PUMP_OUT = -1
    """

    def test_decider_actions(self):
        """ Decider action tests.
        
        Note: margin tests are only required to activate pump, not to determine
        cessation.  I think.
        """
        decider = Decider(100, .05)
        # Arbritrary values set for testing low, even, high levels
        actions = {
            'PUMP_IN': 1,
            'PUMP_OUT': -1,
            'PUMP_OFF': 0
        }
        # Set values to affect pump state out of margin range
        low = 80
        level = 100
        high= 150
        margin_low = 99
        margin_high = 101

        # Pump in state tests:
        # Low -> should be 1 to continue pump in
        self.assertEqual(1, decider.decide(low, actions['PUMP_IN'], actions))
        # Level -> should be 1 to continue pump in 
        self.assertEqual(1, decider.decide(level, actions['PUMP_IN'], actions))
        # High -> should be 0 to stop pumping
        self.assertEqual(0, decider.decide(high, actions['PUMP_IN'], actions))

        # Pump out state tests:
        # Low -> should be 0 to stop pumping
        self.assertEqual(0, decider.decide(low, actions['PUMP_OUT'], actions))
        # Level -> should be -1 to continue pump out
        self.assertEqual(-1, decider.decide(level, actions['PUMP_OUT'], actions))
        # High -> should be -1 to continue pump out
        self.assertEqual(-1, decider.decide(high, actions['PUMP_OUT'], actions))

        # Pump off state tests:
        # Low -> pump should be 1 to pump in
        self.assertEqual(1, decider.decide(low, actions['PUMP_OFF'], actions))
        # Level -> pump should be 0 for staying off
        self.assertEqual(0, decider.decide(level, actions['PUMP_OFF'], actions))
        # High  -> pump should be -1 for pumping out
        self.assertEqual(-1, decider.decide(high, actions['PUMP_OFF'], actions))
        # Margin Low -> pump should be 0 for staying off
        self.assertEqual(0, decider.decide(margin_low, actions['PUMP_OFF'], actions))
        # Margin high -> pump should be 0 for staying off
        self.assertEqual(0, decider.decide(margin_high, actions['PUMP_OFF'], actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_controller_tick(self):
        """ Controller's Tick function unit test. """
        sensor = Sensor('127.0.0.1', 8000)
        pump = Pump('127.0.0.1', 8000)
        decider = Decider(100, .05)
        controller = Controller(sensor, pump, decider)

        