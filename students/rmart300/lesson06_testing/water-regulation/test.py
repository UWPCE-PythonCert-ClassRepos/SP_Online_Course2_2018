"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from waterregulation.pump import Pump
from waterregulation.sensor import Sensor

from waterregulation.controller import Controller
from waterregulation.decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def setUp(self):

        height = 100
        margin = 2
        self.decider = Decider(height, margin)
        self.actions = actions = { 'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1 }

    def test_decider(self):
        """ test all paths of decider class """

        test_case1 = self.decider.decide(97, self.actions['PUMP_OFF'], self.actions)
        test_case2 = self.decider.decide(103, self.actions['PUMP_OFF'], self.actions)
        test_case3 = self.decider.decide(101, self.actions['PUMP_OFF'], self.actions)
        test_case4 = self.decider.decide(101, self.actions['PUMP_IN'], self.actions)
        test_case5 = self.decider.decide(99, self.actions['PUMP_IN'], self.actions)
        test_case6 = self.decider.decide(99, self.actions['PUMP_OUT'], self.actions)
        test_case7 = self.decider.decide(101, self.actions['PUMP_OUT'], self.actions)
        self.assertEqual(self.actions['PUMP_IN'], test_case1)
        self.assertEqual(self.actions['PUMP_OUT'], test_case2)
        self.assertEqual(self.actions['PUMP_OFF'], test_case3)
        self.assertEqual(self.actions['PUMP_OFF'], test_case4)
        self.assertEqual(self.actions['PUMP_IN'], test_case5)
        self.assertEqual(self.actions['PUMP_OFF'], test_case6)
        self.assertEqual(self.actions['PUMP_OUT'], test_case7)

class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):

        height = 100
        margin = 2
        self.decider = Decider(height, margin)
        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1',8001)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.decider.decide = MagicMock(return_value = self.pump.PUMP_IN) 
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_IN)
        self.pump.set_state = MagicMock(return_value = True)
        self.sensor.measure = MagicMock(return_value = 99)
        self.actions = actions = { 'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1 }

    def test_controller(self):

        self.controller.tick()
        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.decider.decide.assert_called_with(99, self.pump.PUMP_IN, self.actions)
 
if __name__ == '__main__':

    unittest.main()
