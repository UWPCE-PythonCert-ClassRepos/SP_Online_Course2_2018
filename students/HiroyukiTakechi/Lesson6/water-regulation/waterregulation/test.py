"""
Hiro Lesson 6 Water-Regulation Assignment: test
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
        """
        Just some example syntax that you might use
        """

        actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1
        }

        target = Decider(10, .1)
        test_off_below = target.decide(9, actions['PUMP_OFF'], actions)
        self.assertEqual(actions['PUMP_IN'], test_off_below)
        test_off_exact = target.decide(10, actions['PUMP_OFF'], actions)
        self.assertEqual(actions['PUMP_OFF'], test_off_exact)
        test_off_above = target.decide(11, actions['PUMP_OFF'], actions)
        self.assertEqual(actions['PUMP_OUT'], test_off_above)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick

    def test_control(self):


        sensor = Sensor('127.0.0.1', 8000)
        sensor.set_state = MagicMock(return_value=True)        
        pump = Pump('127.0.0.1', 8000)
        sensor.set_state = MagicMock(return_value=True)
        decider = Decider(10, .1)
        decider.set_state = MagicMock(return_value=True)
        control = Controller(sensor, pump, decider)
        control.tick().assert_called_with()




