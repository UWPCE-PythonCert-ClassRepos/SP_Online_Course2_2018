#!/usr/bin/env python3
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.target = 100
        self.margin = 0.05
        self.lower_margin = self.target - (self.target * self.margin)
        self.upper_margin = self.target + (self.target * self.margin)
        self.actions = {
            'PUMP_IN':  Pump.PUMP_IN,
            'PUMP_OUT': Pump.PUMP_OUT,
            'PUMP_OFF': Pump.PUMP_OFF,
        }

    def setUp(self):
        self.decider = Decider(self.target, self.margin)

    def test_off_below_margin(self):
        """Test pump off and below margin"""
        curr_state = Pump.PUMP_OFF
        curr_level = self.lower_margin - 5
        next_state = self.decider.decide(curr_level, curr_state, self.actions)

        self.assertEqual(next_state, Pump.PUMP_IN, msg=next_state)

    def test_off_above_margin(self):
        """Test pump off and above margin"""
        curr_state = Pump.PUMP_OFF
        curr_level = self.upper_margin + 5
        next_state = self.decider.decide(curr_level, curr_state, self.actions)

        self.assertEqual(next_state, Pump.PUMP_OUT, msg=next_state)

    def test_off_at_margin(self):
        """Test pump off and within margin"""
        curr_state = Pump.PUMP_OFF
        curr_level = self.lower_margin
        next_state = self.decider.decide(curr_level, curr_state, self.actions)

        self.assertEqual(next_state, Pump.PUMP_OFF, msg=next_state)

    def test_in_above_target(self):
        """Test pump in and above target"""
        curr_state = Pump.PUMP_IN
        curr_level = self.target + 5
        next_state = self.decider.decide(curr_level, curr_state, self.actions)

        self.assertEqual(next_state, Pump.PUMP_OFF, msg=next_state)

    def test_in_below_target(self):
        """Test pump in and below target"""
        curr_state = Pump.PUMP_IN
        curr_level = self.target - 5
        next_state = self.decider.decide(curr_level, curr_state, self.actions)

        self.assertEqual(next_state, Pump.PUMP_IN, msg=next_state)

    def test_out_below_target(self):
        """Test pump out and below target"""
        curr_state = Pump.PUMP_OUT
        curr_level = self.target - 5
        next_state = self.decider.decide(curr_level, curr_state, self.actions)

        self.assertEqual(next_state, Pump.PUMP_OFF, msg=next_state)

    def test_out_above_target(self):
        """Test pump out and above target"""
        curr_state = Pump.PUMP_OUT
        curr_level = self.target + 5
        next_state = self.decider.decide(curr_level, curr_state, self.actions)

        self.assertEqual(next_state, Pump.PUMP_OUT, msg=next_state)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.addr = '127.0.0.1'
        self.port = 8000
        self.target = 100
        self.margin = 0.05
        self.lower_margin = self.target - (self.target * self.margin)
        self.upper_margin = self.target + (self.target * self.margin)
        self.actions = {
            'PUMP_IN':  Pump.PUMP_IN,
            'PUMP_OUT': Pump.PUMP_OUT,
            'PUMP_OFF': Pump.PUMP_OFF,
        }

    def setUp(self):
        self.pump = Pump(self.addr, self.port)
        self.sensor = Sensor(self.addr, self.port)
        self.decider = Decider(self.target, self.margin)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_tick(self):
        """Test controller tick function"""
        self.sensor.measure = MagicMock(return_value=self.target)
        self.pump.get_state = MagicMock(return_value=Pump.PUMP_OFF)
        self.decider.decide = MagicMock(return_value=Pump.PUMP_OFF)
        self.pump.set_state = MagicMock(return_value=True)

        self.controller.tick()

        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.decider.decide.assert_called_with(self.target,
                                               Pump.PUMP_OFF,
                                               self.actions)
        self.pump.set_state.assert_called_with(Pump.PUMP_OFF)


if __name__ == '__main__':
    unittest.main()
