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
    Unit tests for the Decider class.
    """

    def test_decider(self):
        """Method for DeciderTests. Should test every decider scenario."""

        actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1
        }

        di = Decider(100, 0.05)

        scen1 = di.decide(125, actions['PUMP_OFF'], actions)
        scen2 = di.decide(75, actions['PUMP_OFF'], actions)
        scen3 = di.decide(100, actions['PUMP_OFF'], actions)
        scen4 = di.decide(125, actions['PUMP_IN'], actions)
        scen5 = di.decide(75, actions['PUMP_IN'], actions)
        scen6 = di.decide(75, actions['PUMP_OUT'], actions)
        scen7 = di.decide(125, actions['PUMP_OFF'], actions)

        self.assertEqual(actions['PUMP_OUT'], scen1)
        self.assertEqual(actions['PUMP_IN'], scen2)
        self.assertEqual(actions['PUMP_OFF'], scen3)
        self.assertEqual(actions['PUMP_OFF'], scen4)
        self.assertEqual(actions['PUMP_IN'], scen5)
        self.assertEqual(actions['PUMP_OFF'], scen6)
        self.assertEqual(actions['PUMP_OUT'], scen7)

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
    Unit tests for the Controller class.
    """

    def test_tick(self):
        """Test method for controller.tick method."""

        di = Decider(100, 0.05)
        pi = Pump('127.0.0.1', '8000')