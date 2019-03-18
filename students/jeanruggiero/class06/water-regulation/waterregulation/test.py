"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from .controller import Controller
from .decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    decider = Decider(10, 1)
    pump = MagicMock()
    pump.PUMP_IN = 1
    pump.PUMP_OFF = 0
    pump.PUMP_OUT = -1

    actions = {
        'PUMP_IN': pump.PUMP_IN,
        'PUMP_OUT': pump.PUMP_OUT,
        'PUMP_OFF': pump.PUMP_OFF,
    }

    def test_decider_off_below(self):
        """Test decider with pump off, level below target."""
        self.assertEqual(self.decider.decide(5, self.pump.PUMP_OFF,
                                             self.actions), self.pump.PUMP_IN)

    def test_decider_off_above(self):
        """Test decider with pump off, level above target."""
        self.assertEqual(self.decider.decide(15, self.pump.PUMP_OFF,
                                             self.actions), self.pump.PUMP_OUT)

    def test_decider_off_between(self):
        """Test decider with pump off, level between target."""
        self.assertEqual(self.decider.decide(9, self.pump.PUMP_OFF,
                                             self.actions), self.pump.PUMP_OFF)
        self.assertEqual(self.decider.decide(10, self.pump.PUMP_OFF,
                                             self.actions), self.pump.PUMP_OFF)
        self.assertEqual(self.decider.decide(11, self.pump.PUMP_OFF,
                                             self.actions), self.pump.PUMP_OFF)

    def test_decider_in(self):
        """Test decider with pump in."""
        self.assertEqual(self.decider.decide(11, self.pump.PUMP_IN,
                                             self.actions), self.pump.PUMP_OFF)
        self.assertEqual(self.decider.decide(9, self.pump.PUMP_IN,
                                             self.actions), self.pump.PUMP_IN)

    def test_decider_out(self):
        """Test decider with pump out."""
        self.assertEqual(self.decider.decide(9, self.pump.PUMP_OUT,
                                             self.actions), self.pump.PUMP_OFF)
        self.assertEqual(self.decider.decide(12, self.pump.PUMP_OUT,
                                             self.actions), self.pump.PUMP_OUT)

    def test_decider_error(self):
        """Test decider error state."""
        with self.assertRaises(KeyError):
            self.decider.decide(9, 2, self.actions)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    decider = MagicMock()
    decider.decide = MagicMock(return_value=1)
    sensor = MagicMock()
    sensor.measure = MagicMock(return_value=5)
    pump = MagicMock()
    pump.get_state = MagicMock(return_value=0)
    pump.set_state = MagicMock(return_value=True)

    controller = Controller(sensor, pump, decider)

    def test_tick(self):
        """Controller.tick() unit test."""
        self.assertEqual(self.controller.tick(), True)
        self.sensor.measure.assert_called()
        self.pump.get_state.assert_called()

        self.decider.decide.assert_called_with(self.sensor.measure(),
                                               self.pump.get_state(),
                                               self.controller.actions)
        self.pump.set_state.assert_called_with(self.decider.decide())
