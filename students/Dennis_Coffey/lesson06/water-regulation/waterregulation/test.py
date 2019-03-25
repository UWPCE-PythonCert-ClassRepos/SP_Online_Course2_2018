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
        """
        Sets up pump, sensor, decider and controller for use with
        unit tests.
        """

        margin = self.decider.margin
        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1', 8000)
        self.decider = Decider(target_height=100, margin=0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.low_height = self.decider.target_height * (1 - 2 * margin)
        self.high_height = self.decider.target_height * (1 + 2 * margin)
        self.upper_margin_height = self.decider.target_height * (1 + margin)

    def test_off_below_margin(self):
        """
        Test if the pump is off and the height is below the margin region,
        then the pump should be turned to PUMP_IN - Situation 1.
        """
        pump_state = "PUMP_OFF"
        self.assertEqual(self.controller.actions['PUMP_IN'],
                         self.decider.decide(current_height=self.low_height,
                                             current_action=pump_state,
                                             actions=self.controller.actions))

    def test_off__above_margin(self):
        """
        Test if the pump is off and the height is above the margin region,
             then the pump should be turned to PUMP_OUT - Situation 2.
        """
        pump_state = "PUMP_OFF"
        self.assertEqual(self.controller.actions['PUMP_OUT'],
                         self.decider.decide(current_height=self.high_height,
                                             current_action=pump_state,
                                             actions=self.controller.actions))

    def test_off_within_margin(self):
        """
        Test if the pump is off and the height is within the margin region,
            then the pump shall remain at
            PUMP_OFF - Situation 3.
        """
        pump_state = "PUMP_OFF"
        target = self.decider.target_height
        self.assertEqual(self.controller.actions['PUMP_OFF'],
                         self.decider.decide(current_height=target,
                                             current_action=pump_state,
                                             actions=self.controller.actions))

    def test_off_on_margin(self):
        """
        Test if the pump is off and the height is on
             the exact boundary of the margin region, then the pump shall
             remain at PUMP_OFF - Situation 3.
        """
        pump_state = "PUMP_OFF"
        upper = self.upper_margin_height
        self.assertEqual(self.controller.actions['PUMP_OFF'],
                         self.decider.decide(current_height=upper,
                                             current_action=pump_state,
                                             actions=self.controller.actions))

    def test_in_above_target(self):
        """
        Test the pump is performing PUMP_IN and the height is above the target
             height, then the pump shall be turned to PUMP_OFF, otherwise the
             pump shall remain at PUMP_IN - Situation 4.
        """
        pump_state = "PUMP_IN"
        upper = self.upper_margin_height
        self.assertEqual(self.controller.actions['PUMP_OFF'],
                         self.decider.decide(current_height=upper,
                                             current_action=pump_state,
                                             actions=self.controller.actions))

    def test_in_below_target(self):
        """
        Test the pump is performing PUMP_IN and the height is below the target
             height, then pump shall remain at PUMP_IN - Situation 4.
        """
        pump_state = "PUMP_IN"
        self.assertEqual(self.controller.actions['PUMP_IN'],
                         self.decider.decide(current_height=self.low_height,
                                             current_action=pump_state,
                                             actions=self.controller.actions))

    def test_out_below_target(self):
        """
        the pump is performing PUMP_OUT and the height is below the target
             height, then the pump shall be turned to PUMP_OFF, otherwise,
             the pump shall remain at PUMP_OUT - Situation 5.
        """
        pump_state = "PUMP_OUT"
        self.assertEqual(self.controller.actions['PUMP_OFF'],
                         self.decider.decide(current_height=self.low_height,
                                             current_action=pump_state,
                                             actions=self.controller.actions))

    def test_out_above_target(self):
        """
        Test the pump is performing PUMP_OUT and the height is above the target
             height, then pump shall remain at PUMP_OUT - Situation 5.
        """
        pump_state = "PUMP_OUT"
        upper = self.upper_margin_height
        self.assertEqual(self.controller.actions['PUMP_OUT'],
                         self.decider.decide(current_height=upper,
                                             current_action=pump_state,
                                             actions=self.controller.actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        """
        Sets up pump, sensor, decider and controller for use with
        unit tests.
        """
        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1', 8000)
        self.decider = Decider(target_height=100, margin=0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_tick(self):
        """
        Testing Controller.tick
        """
        current_height = 100
        current_pump_state = 'PUMP_OFF'
        self.sensor.measure = MagicMock(return_value=current_height)
        self.pump.get_state = MagicMock(return_value=current_pump_state)
        self.decider.decide = MagicMock(return_value='PUMP_OFF')
        self.pump.set_state = MagicMock(return_value=True)

        self.controller.tick()

        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.decider.decide.assert_called_with(current_height,
                                               'PUMP_OFF',
                                               self.controller.actions)
