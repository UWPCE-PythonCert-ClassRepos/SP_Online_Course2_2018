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

    def test_decider_decide(self):
        actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1
        }

        decider = Decider(100, .10)

        self.assertEqual(1, decider.decide(89, 'PUMP_OFF', actions))
        self.assertEqual(-1, decider.decide(111, 'PUMP_OFF', actions))
        self.assertEqual(0, decider.decide(95, 'PUMP_OFF', actions))
        self.assertEqual(0, decider.decide(101, 'PUMP_IN', actions))
        self.assertEqual(1, decider.decide(99, 'PUMP_IN', actions))
        self.assertEqual(0, decider.decide(99, 'PUMP_OUT', actions))
        self.assertEqual(-1, decider.decide(101, 'PUMP_OUT', actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick

    pass
