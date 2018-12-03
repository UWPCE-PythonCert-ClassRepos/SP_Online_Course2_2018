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
    Unit tests for the Decider class
    """

    def test_decider_decide(self):
        """
        Test Decdider's decide method
        """
        decider = Decider(100, .1)
        test1 = decider.decide(85, ACTIONS['PUMP_OFF'], ACTIONS)
        test2 = decider.decide(115, ACTIONS['PUMP_OFF'], ACTIONS)
        test3 = decider.decide(105, ACTIONS['PUMP_OFF'], ACTIONS)
        test4 = decider.decide(105, ACTIONS['PUMP_IN'], ACTIONS)
        test5 = decider.decide(95, ACTIONS['PUMP_IN'], ACTIONS)
        test6 = decider.decide(95, ACTIONS['PUMP_OUT'], ACTIONS)
        test7 = decider.decide(105, ACTIONS['PUMP_OUT'], ACTIONS)
        self.assertEqual(ACTIONS['PUMP_IN'], test1)
        self.assertEqual(ACTIONS['PUMP_OUT'], test2)
        self.assertEqual(ACTIONS['PUMP_OFF'], test3)
        self.assertEqual(ACTIONS['PUMP_OFF'], test4)
        self.assertEqual(ACTIONS['PUMP_IN'], test5)
        self.assertEqual(ACTIONS['PUMP_OFF'], test6)
        self.assertEqual(ACTIONS['PUMP_OUT'], test7)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick(self):
        """
        Test Controller tick
        """
        pump = Pump('127.0.0.1', 8080)
        sensor = Sensor('127.0.0.1', 8083)
        decider = Decider(100, .1)
        controller = Controller(sensor, pump, decider)
        sensor.measure = MagicMock(return_value=95)
        pump.get_state = MagicMock(return_value=pump.PUMP_IN)
        decider.decide = MagicMock(return_value=pump.PUMP_IN)
        pump.set_state = MagicMock(return_value=True)

        controller.tick()
        sensor.measure.assert_called_with()
        pump.get_state.assert_called_with()
        decider.decide.assert_called_with(95, pump.PUMP_IN, ACTIONS)
