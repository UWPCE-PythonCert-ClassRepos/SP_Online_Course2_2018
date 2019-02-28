"""
Unit tests for the water-regulation module
"""

from unittest import TestCase
from unittest.mock import MagicMock

from pump.pump import Pump
from sensor.sensor import Sensor

from .controller import Controller
from .decider import Decider


class DeciderTests(TestCase):
    """
    Unit tests for the Decider class
    """
    def setUp(self):
        """
        Setup for test_decider.
        """
        self.decider = Decider(30, 0.05)
        self.actions = {
            "PUMP_IN": 1,
            "PUMP_OFF": 0,
            "PUMP_OUT": -1
            }

    def test_decide(self):
        """test Decider class"""
        self.assertEqual(1, self.decider.decide(10, "PUMP_OFF", self.actions))
        self.assertEqual(-1, self.decider.decide(50, "PUMP_OFF", self.actions))
        self.assertEqual(0, self.decider.decide(30, "PUMP_OFF", self.actions))
        self.assertEqual(0, self.decider.decide(40, "PUMP_IN", self.actions))
        self.assertEqual(1, self.decider.decide(28, "PUMP_IN", self.actions))
        self.assertEqual(0, self.decider.decide(15, "PUMP_OUT", self.actions))
        self.assertEqual(-1, self.decider.decide(34, "PUMP_OUT", self.actions))


class ControllerTests(TestCase):
    """
    Unit tests for the Controller class.
    """

    def setUp(self):
        """
        Setup for test_tick
        """
        self.sensor = Sensor('127.0.0.1', '8000')
        self.pump = Pump('127.0.0.1', '8001')
        self.decider = Decider(30, 0.05)
        self.sensor.measure = MagicMock(return_value=True)
        self.pump.set_state = MagicMock(return_value=True)
        self.pump.get_state = MagicMock(return_value="PUMP_IN")
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_tick(self):
        """
        Test Controller module.
        """
        self.assertEqual(True, self.controller.tick())
