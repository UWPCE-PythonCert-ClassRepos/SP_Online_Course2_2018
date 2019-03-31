"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock
from unittest import TestCase

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class DeciderTests(TestCase):
    """
    Unit tests for the Decider class
    """

    def setUp(self):
        """
        Setup for Decider tests
        """
        self.decider = Decider(100, 0.5)
        self.actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1,
        }

    def test_decide_pump_off(self):
        """
        PUMP_OFF initial state for each sensor level in the tank
        """
        self.assertEqual(
            self.decider.decide(99.40, self.actions['PUMP_OFF'], self.actions),
            1)
        self.assertEqual(
            self.decider.decide(99.50, self.actions['PUMP_OFF'], self.actions),
            0)
        self.assertEqual(
            self.decider.decide(99.75, self.actions['PUMP_OFF'], self.actions),
            0)
        self.assertEqual(
            self.decider.decide(100.00, self.actions['PUMP_OFF'],
                                self.actions),
            0)
        self.assertEqual(
            self.decider.decide(100.25, self.actions['PUMP_OFF'],
                                self.actions),
            0)
        self.assertEqual(
            self.decider.decide(100.50, self.actions['PUMP_OFF'],
                                self.actions),
            0)
        self.assertEqual(
            self.decider.decide(100.60, self.actions['PUMP_OFF'],
                                self.actions),
            -1)

    def test_decide_pump_in(self):
        """
        PUMP_IN initial state for each sensor level in the tank
        """
        self.assertEqual(
            self.decider.decide(99.40, self.actions['PUMP_IN'], self.actions),
            1)
        self.assertEqual(
            self.decider.decide(99.50, self.actions['PUMP_IN'], self.actions),
            1)
        self.assertEqual(
            self.decider.decide(99.75, self.actions['PUMP_IN'], self.actions),
            1)
        self.assertEqual(
            self.decider.decide(100.00, self.actions['PUMP_IN'], self.actions),
            1)
        self.assertEqual(
            self.decider.decide(100.25, self.actions['PUMP_IN'], self.actions),
            0)
        self.assertEqual(
            self.decider.decide(100.50, self.actions['PUMP_IN'], self.actions),
            0)
        self.assertEqual(
            self.decider.decide(100.60, self.actions['PUMP_IN'], self.actions),
            0)

    def test_decide_pump_out(self):
        """
        PUMP_OUT initial state for each sensor level in the tank
        """
        self.assertEqual(
            self.decider.decide(99.40, self.actions['PUMP_OUT'], self.actions),
            0)
        self.assertEqual(
            self.decider.decide(99.50, self.actions['PUMP_OUT'], self.actions),
            0)
        self.assertEqual(
            self.decider.decide(99.75, self.actions['PUMP_OUT'], self.actions),
            0)
        self.assertEqual(
            self.decider.decide(100.00, self.actions['PUMP_OUT'],
                                self.actions),
            -1)
        self.assertEqual(
            self.decider.decide(100.25, self.actions['PUMP_OUT'],
                                self.actions),
            -1)
        self.assertEqual(
            self.decider.decide(100.50, self.actions['PUMP_OUT'],
                                self.actions),
            -1)
        self.assertEqual(
            self.decider.decide(100.60, self.actions['PUMP_OUT'],
                                self.actions),
            -1)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1', 7000)
        self.decider = Decider(100, 0.5)
        self.actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1,
        }

    def test_controller_pass(self):
        """
        Test for controller.tick() when setting the new pump state passes
        """
        self.pump.set_state = MagicMock(return_value=True)
        sensor_input = [99.4, 99.5, 99.75, 100, 100.25, 100.5, 100.6]

        for pump_state in self.actions:
            for sensor_value in sensor_input:
                self.pump.get_state = MagicMock(return_value=pump_state)
                self.sensor.measure = MagicMock(return_value=sensor_value)

                self.decider.decide = MagicMock(return_value=pump_state)
                test_controller = Controller(self.sensor, self.pump,
                                             self.decider)
                test_controller.tick()

                self.decider.decide.assert_called_with(sensor_value,
                                                       pump_state,
                                                       self.actions)
                self.pump.set_state.assert_called_with(pump_state)
                self.pump.get_state.assert_called_with()
                self.sensor.measure.assert_called_with()

    def test_controller_fails(self):
        """
        Test for controller.tick() when the state of new pump fails
        """
        self.pump.set_state = MagicMock(return_value=False)
        sensor_input = [99.4, 99.5, 99.75, 100, 100.25, 100.5, 100.6]

        for pump_state in self.actions:
            for sensor_value in sensor_input:
                self.pump.get_state = MagicMock(return_value=pump_state)
                self.sensor.measure = MagicMock(return_value=sensor_value)

                self.decider.decide = MagicMock(return_value=pump_state)
                test_controller = Controller(self.sensor, self.pump,
                                             self.decider)
                test_controller.tick()

                self.decider.decide.assert_called_with(sensor_value,
                                                       pump_state,
                                                       self.actions)
                self.pump.set_state.assert_called_with(pump_state)
                self.pump.get_state.assert_called_with()
                self.sensor.measure.assert_called_with()
