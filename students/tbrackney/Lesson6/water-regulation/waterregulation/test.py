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

    # TODO: write a test or tests for each of the behaviors defined for
    #       Decider.decide

    def setup(self):
        """Create dummy instance"""
        self.decider = Decider(100, 0.05)
        self.actions = {"PUMP_IN": 1, "PUMP_OUT": -1, "PUMP_OFF": 0}


    def test_dummy(self):
        """
        Just some example syntax that you might use
        """

        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)

        self.fail("Remove this test.")

    def test_pump_in(self):
        call = self.decider.decide(90, self.actions['PUMP_OFF'], self.actions)
        expected = self.actions['PUMP_IN']
        self.assertEqual(call, expected)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick

    pass
