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
    def test_actions(self):
        """
        Just some example syntax that you might use
        """
        actions = {
            'PUMP_IN': Pump.PUMP_IN,
            'PUMP_OUT': Pump.PUMP_OUT,
            'PUMP_OFF': Pump.PUMP_OFF
            }

        pump_off = Pump.PUMP_OFF
        pump_in = Pump.PUMP_IN
        pump_out = Pump.PUMP_OUT
        target = 100
        margin = 0.05
        above = 106
        below = 94
        meet = 100

        decider = Decider(target, margin)
        self.assertEqual(decider.decide(below, pump_off, actions), pump_in)
        self.assertEqual(decider.decide(above, pump_off, actions), pump_out)
        self.assertEqual(decider.decide(meet, pump_off, actions), pump_off)
        self.assertEqual(decider.decide(above, pump_in, actions), pump_off)
        self.assertEqual(decider.decide(below, pump_in, actions), pump_in)
        self.assertEqual(decider.decide(meet, pump_in, actions), pump_in)
        self.assertEqual(decider.decide(above, pump_out, actions), pump_out)
        self.assertEqual(decider.decide(below, pump_out, actions), pump_off)
        self.assertEqual(decider.decide(meet, pump_out, actions), pump_out)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick

    pass
