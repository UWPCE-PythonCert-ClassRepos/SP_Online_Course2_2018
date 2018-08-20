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

    def setUp(self):

        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)

        self.actions = {
            'PUMP_IN': pump.PUMP_IN,
            'PUMP_OUT': pump.PUMP_OUT,
            'PUMP_OFF': pump.PUMP_OFF,
        }

    def test_decider(self):
        """
        Test that the decider function correctly assigns the next state
        """

        decider = Decider(100, .05)
        scen1 = decider.decide(90, self.actions['PUMP_OFF'], self.actions)
        self.assertEqual(scen1, self.actions['PUMP_IN'])
        scen2 = decider.decide(110, self.actions['PUMP_OFF'], self.actions)
        self.assertEqual(scen2, self.actions['PUMP_OUT'])
        scen3a = decider.decide(95, self.actions['PUMP_OFF'], self.actions)
        self.assertEqual(scen3a, self.actions['PUMP_OFF'])
        scen3b = decider.decide(105, self.actions['PUMP_OFF'], self.actions)
        self.assertEqual(scen3b, self.actions['PUMP_OFF'])
        scen3c = decider.decide(102, self.actions['PUMP_OFF'], self.actions)
        self.assertEqual(scen3c, self.actions['PUMP_OFF'])
        scen4a = decider.decide(101, self.actions['PUMP_IN'], self.actions)
        self.assertEqual(scen4a, self.actions['PUMP_OFF'])
        scen4b = decider.decide(85, self.actions['PUMP_IN'], self.actions)
        self.assertEqual(scen4b, self.actions['PUMP_IN'])
        scen5a = decider.decide(99, self.actions['PUMP_OUT'], self.actions)
        self.assertEqual(scen5a, self.actions['PUMP_OFF'])
        scen5b = decider.decide(102, self.actions['PUMP_OUT'], self.actions)
        self.assertEqual(scen5b, self.actions['PUMP_OUT'])


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):

        self.pump = Pump('127.0.0.1', 8000)
        self.pump.set_state = MagicMock(return_value=True)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OFF)

        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

        self.sensor = Sensor('127.0.0.1', 8000)
        self.sensor.measure = MagicMock(return_value=95)

        self.decider = Decider(100, .02)
        self.decider.decide = MagicMock(return_value=self.pump.PUMP_IN)

        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_controller(self):
        """
        Test that the controller function correctly calls the decider function
        """

        self.assertEqual(self.controller.tick(), True)
        self.decider.decide.assert_called_with(95,
                                               self.pump.PUMP_OFF,
                                               self.actions)
