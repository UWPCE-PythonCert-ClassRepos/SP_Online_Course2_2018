"""
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

    def setUp(self):
        """ set up class variables """

        height = 100
        margin = 2
        self.decider = Decider(height, margin)
        self.actions = {'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1}

    def test_decider(self):
        """ test all paths of decider class """

        test1 = self.decider.decide(97, self.actions['PUMP_OFF'], self.actions)
        test2 = self.decider.decide(103, self.actions['PUMP_OFF'], self.actions)
        test3 = self.decider.decide(101, self.actions['PUMP_OFF'], self.actions)
        test4 = self.decider.decide(101, self.actions['PUMP_IN'], self.actions)
        test5 = self.decider.decide(99, self.actions['PUMP_IN'], self.actions)
        test6 = self.decider.decide(99, self.actions['PUMP_OUT'], self.actions)
        test7 = self.decider.decide(101, self.actions['PUMP_OUT'], self.actions)
        self.assertEqual(self.actions['PUMP_IN'], test1)
        self.assertEqual(self.actions['PUMP_OUT'], test2)
        self.assertEqual(self.actions['PUMP_OFF'], test3)
        self.assertEqual(self.actions['PUMP_OFF'], test4)
        self.assertEqual(self.actions['PUMP_IN'], test5)
        self.assertEqual(self.actions['PUMP_OFF'], test6)
        self.assertEqual(self.actions['PUMP_OUT'], test7)

class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        """ set up class variables """

        height = 100
        margin = 2
        self.decider = Decider(height, margin)
        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1', 8001)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.decider.decide = MagicMock(return_value=self.pump.PUMP_IN)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_IN)
        self.pump.set_state = MagicMock(return_value=True)
        self.sensor.measure = MagicMock(return_value=99)
        self.actions = {'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1}

    def test_controller(self):
        """ test tick function """

        self.controller.tick()
        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.decider.decide.assert_called_with(99, self.pump.PUMP_IN, self.actions)


if __name__ == '__main__':

    unittest.main()
