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

    def test_decide(self):

        actions = {'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1}

        target = Decider(100, .05)

        self.assertEqual(1, target.decide(94, actions['PUMP_OFF'], actions))
        self.assertEqual(-1, target.decide(106, actions['PUMP_OFF'], actions))
        self.assertEqual(0, target.decide(104, actions['PUMP_OFF'], actions))
        self.assertEqual(0, target.decide(106, actions['PUMP_IN'], actions))
        self.assertEqual(1, target.decide(93, actions['PUMP_IN'], actions))
        self.assertEqual(0, target.decide(93, actions['PUMP_OUT'], actions))
        self.assertEqual(-1, target.decide(112, actions['PUMP_OUT'], actions))



class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick

    pass
