"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock
from urllib.error import URLError

from pump import Pump
from sensor import Sensor

from controller import Controller
from decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def test_decide(self):
        """
        Test decider's decide method
        """
        dec = Decider(100, .05)
        actions = {
            'PUMP_IN': 1,
            'PUMP_OUT': -1,
            'PUMP_OFF': 0,
        }
        above = 110
        below = 90
        inside = 99
        self.assertEqual(1, dec.decide(below, 0, actions))
        self.assertEqual(1, dec.decide(below, 1, actions))
        self.assertEqual(-1, dec.decide(above, 0, actions))
        self.assertEqual(-1, dec.decide(above, -1, actions))
        self.assertEqual(0, dec.decide(inside, 0, actions))
        self.assertEqual(0, dec.decide(above, 1, actions))
        self.assertEqual(0, dec.decide(below, -1, actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        """
        Sets up controller.
        """
        self.sensor = Sensor("127.0.0.1", "8000")
        self.pump = Pump("127.0.0.1", "8000")
        self.decider = Decider(100, .05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_tick(self):
        """
        Test if decider.decide and pump.set_state are called with the correct
        parameters after controller.tick()
        """
        self.sensor.measure = MagicMock(return_value=100)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OFF)
        self.decider.decide = MagicMock(return_value=self.pump.PUMP_IN)
        self.pump.set_state = MagicMock(return_value=True)

        self.controller.tick()
        self.decider.decide.assert_called_with(100, self.pump.PUMP_OFF,
                                               self.controller.actions)
        self.pump.set_state.assert_called_with(self.pump.PUMP_IN)

    def test_raise_url_controller(self):
        """
        Test controller.tick raises the sensor.measure URLError
        """
        with self.assertRaises(URLError):
            self.controller.tick()

    def test_raise_url_sensor(self):
        """
        Test sensor.measure raises URLError
        """
        with self.assertRaises(URLError):
            self.sensor.measure()

    def test_raise_url_pump_get(self):
        """
        Test pump.get_state raises URLError
        """
        self.sensor.measure = MagicMock(return_value=100)
        with self.assertRaises(URLError):
            self.pump.get_state()

    def test_raise_url_pump_set(self):
        """
        Test pump.set_state raises URLError
        """
        self.sensor.measure = MagicMock(return_value=100)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OFF)
        with self.assertRaises(URLError):
            self.pump.set_state(self.pump.PUMP_OFF)
