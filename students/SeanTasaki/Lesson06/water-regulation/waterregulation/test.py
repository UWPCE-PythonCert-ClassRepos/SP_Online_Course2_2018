"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock
from pump import Pump
from sensor import Sensor
from controller import Controller
from decider import Decider

class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def test_dummy(self):
        """
        Just some example syntax that you might use
        """

        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)

        actions = {
            'PUMP_IN': Pump.PUMP_IN,
            'PUMP_OUT': Pump.PUMP_OUT,
            'PUMP_OFF': Pump.PUMP_OFF
            }


        target = 100
        margin = 5
        above = 107
        below = 92
        between = 102

        decider = Decider(target, margin)

        pump_off = decider.decide_pump_action(0, actions)
        pump_in = decider.decide_pump_action(1, actions)
        pump_out = decider.decide_pump_action(-1, actions)
        height_above = decider.height_checker(above)
        height_below = decider.height_checker(below)
        height_between = decider.height_checker(between)

        self.assertEqual(pump_off(height_above), Pump.PUMP_OUT)
        self.assertEqual(pump_off(height_below), Pump.PUMP_IN)
        self.assertEqual(pump_off(height_between), Pump.PUMP_OFF)
        self.assertEqual(pump_in(height_above), Pump.PUMP_OFF)
        self.assertEqual(pump_in(height_below), Pump.PUMP_IN)
        self.assertEqual(pump_in(height_between), Pump.PUMP_IN)
        self.assertEqual(pump_out(height_above), Pump.PUMP_OUT)
        self.assertEqual(pump_out(height_below), Pump.PUMP_OFF)
        self.assertEqual(pump_out(height_between), Pump.PUMP_OUT)

class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick(self):
        """Method docstring."""
        ACTIONS = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1
            }

        pump_address = Pump('127.0.0.1', 8000)
        sensor_address = Sensor('127.0.0.1', 8000)
        decider_vals = Decider(100, 5)
        controller_all = Controller(sensor_address, pump_address, decider_vals)

        sensor_address.measure = MagicMock(return_value=90)
        pump_address.get_state = MagicMock(return_value=pump_address.PUMP_OFF)
        decider_vals.decide_pump_action = MagicMock(return_value=pump_address.PUMP_IN)
        pump_address.set_state = MagicMock(return_value=True)
        controller_all.tick()
        pump_address.get_state = MagicMock(return_value=pump_address.PUMP_IN)
        controller_all.tick()
        pump_address.get_state = MagicMock(return_value=pump_address.PUMP_OUT)
        controller_all.tick()

        sensor_address.measure.assert_called_with()
        pump_address.get_state.assert_called_with()
        pump_address.set_state.assert_called_with(pump_address.PUMP_OFF)
