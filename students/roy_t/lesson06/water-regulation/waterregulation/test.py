"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock
import sys
sys.path.insert(0, 'C:\\Users\\roy\\Documents\\uw_python\\SP_Online_Course2_2018\\students\\roy_t\\lesson06\\water-regulation\\')

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

    def setUp(self):
        """Set up each test with an actions dict"""
        self.actions = {'PUMP_IN': 1,
                        'PUMP_OFF': 0,
                        'PUMP_OUT': -1}

    def test_decider_returns_correct_decisions(self):
        """1. If the pump is off and the height is below the margin region, then the pump should be turned to PUMP_IN."""
        decider = Decider(100, .05)
        self.assertEqual(0, decider.decide(190, 0, self.actions))

    # def test_dummy(self):
    #     """
    #     Just some example syntax that you might use
    #     """
    #
    #     pump = Pump('127.0.0.1', 8000)
    #     pump.set_state = MagicMock(return_value=True)
    #
    #     self.fail("Remove this test.")


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick

    pass
