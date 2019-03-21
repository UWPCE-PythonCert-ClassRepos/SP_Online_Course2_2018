"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider

ACTIONS = {
    'PUMP_IN': 1,
    'PUMP_OFF': 0,
    'PUMP_OUT': -1
    }


class DeciderTests(unittest.TestCase):
    """
    Unit tests for Decider class
    """

    def test_decider_decide(self):
        """
        Test cases for decide method of Decider module
        """
        decider = Decider(100, .1)
        # Run Tests
        test1 = decider.decide(50, ACTIONS['PUMP_OFF'], ACTIONS)
        test2 = decider.decide(150, ACTIONS['PUMP_OFF'], ACTIONS)
        test3 = decider.decide(101, ACTIONS['PUMP_OFF'], ACTIONS)
        test4 = decider.decide(99, ACTIONS['PUMP_OFF'], ACTIONS)
        test5 = decider.decide(110, ACTIONS['PUMP_IN'], ACTIONS)
        test6 = decider.decide(95, ACTIONS['PUMP_IN'], ACTIONS)
        test7 = decider.decide(99, ACTIONS['PUMP_OUT'], ACTIONS)
        test8 = decider.decide(110, ACTIONS['PUMP_OUT'], ACTIONS)
        # Check Results
        self.assertEqual(ACTIONS['PUMP_IN'], test1)
        self.assertEqual(ACTIONS['PUMP_OUT'], test2)
        self.assertEqual(ACTIONS['PUMP_OFF'], test3)
        self.assertEqual(ACTIONS['PUMP_OFF'], test4)
        self.assertEqual(ACTIONS['PUMP_OFF'], test5)
        self.assertEqual(ACTIONS['PUMP_IN'], test6)
        self.assertEqual(ACTIONS['PUMP_OFF'], test7)
        self.assertEqual(ACTIONS['PUMP_OUT'], test8)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for Controller class
    """

    def test_tick(self):
        """
        Test Controller tick function
        """
        pump = Pump('127.0.0.1', 8080)
        sensor = Sensor('127.0.0.1', 8083)
        decider = Decider(100, .1)
        controller = Controller(sensor, pump, decider)
        sensor.measure = MagicMock(return_value=127)
        pump.get_state = MagicMock(return_value=pump.PUMP_IN)
        decider.decide = MagicMock(return_value=pump.PUMP_IN)
        pump.set_state = MagicMock(return_value=True)

        controller.tick()
        sensor.measure.assert_called_with()
        pump.get_state.assert_called_with()
        decider.decide.assert_called_with(127, pump.PUMP_IN, ACTIONS)
