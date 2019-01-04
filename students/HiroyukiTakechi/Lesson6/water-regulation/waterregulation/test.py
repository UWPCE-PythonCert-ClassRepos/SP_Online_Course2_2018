"""
Hiro Lesson 6 Water-Regulation Assignment: test
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from .pump import Pump
from .sensor import Sensor

from .controller import Controller
from .decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Decider.decide

    def test_decide(self):
        """
        Just some example syntax that you might use
        """

        actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1
        }

        target = Decider(100, .10)
        target_test_a = target.decide(50, actions['PUMP_OFF'], actions)
        target_test_b = target.decide(200, actions['PUMP_OFF'], actions)
        target_test_c = target.decide(105, actions['PUMP_OFF'], actions)
        target_test_d = target.decide(200, actions['PUMP_IN'], actions)
        target_test_e = target.decide(95, actions['PUMP_IN'], actions)
        target_test_f = target.decide(95, actions['PUMP_OUT'], actions)
        target_test_g = target.decide(105, actions['PUMP_OUT'], actions)
        self.assertEqual(actions['PUMP_IN'], target_test_a)
        self.assertEqual(actions['PUMP_OUT'], target_test_b)
        self.assertEqual(actions['PUMP_OFF'], target_test_c)
        self.assertEqual(actions['PUMP_OFF'], target_test_d)
        self.assertEqual(actions['PUMP_IN'], target_test_e)
        self.assertEqual(actions['PUMP_OFF'], target_test_f)
        self.assertEqual(actions['PUMP_OUT'], target_test_g)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick

    def test_control(self):
        """
        Using Ghassan's code as an template
        """
        actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1
        }

        p = Pump('127.0.0.1', 8080)
        s = Sensor('127.0.0.1', 8083)
        d = Decider(100, .10)
        c = Controller(s, p, d)
        s.measure = MagicMock(return_value=95)
        p.get_state = MagicMock(return_value=p.PUMP_IN)
        d.decide = MagicMock(return_value=p.PUMP_IN)
        p.set_state = MagicMock(return_value=True)
        c.tick()
        s.measure.assert_called_with()
        p.get_state.assert_called_with()
        d.decide.assert_called_with(95, p.PUMP_IN, actions)
