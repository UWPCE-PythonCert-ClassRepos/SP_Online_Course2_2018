#!/usr/bin/env python3
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
            Sets the necessary varialbles to test the Decider class
        """

        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)
        self.new_decider = Decider(100, .10)

        self.actions = {
            'PUMP_IN': pump.PUMP_IN,
            'PUMP_OUT': pump.PUMP_OUT,
            'PUMP_OFF': pump.PUMP_OFF,
        }

    def test_behavior_1(self):
        """
        Test 1 - If the pump is off and the height is below the margin region,
            then the pump should be turned to PUMP_IN.
        """

        behavior_1 = self.new_decider.decide(89, self.actions['PUMP_OFF'],
                                             self.actions)
        self.assertEqual(self.actions['PUMP_IN'], behavior_1)

    def test_behavior_2(self):
        """
        Test 2 - If the pump is off and the height is above the margin region,
                then the pump should be turned to PUMP_OUT.
        """

        behavior_2 = self.new_decider.decide(111, self.actions['PUMP_OFF'],
                                             self.actions)
        self.assertEqual(self.actions['PUMP_OUT'], behavior_2)

    def test_behavior_3(self):
        """
        Test 3 - If the pump is off and the height is within the margin
            region or on the exact boundary of the margin region,
            then the pump shall remain at PUMP_OFF.
        """

        behavior_3 = self.new_decider.decide(100, self.actions['PUMP_OFF'],
                                             self.actions)
        self.assertEqual(self.actions['PUMP_OFF'], behavior_3)

    def test_behavior_4(self):
        """
        Test 4 - If the pump is performing PUMP_IN and the height is above
            the target height, then the pump shall be turned to PUMP_OFF,
            otherwise the pump shall remain at PUMP_IN.
        """

        behavior_4a = self.new_decider.decide(101, self.actions['PUMP_IN'],
                                              self.actions)
        self.assertEqual(self.actions['PUMP_OFF'], behavior_4a)

        behavior_4b = self.new_decider.decide(99, self.actions['PUMP_IN'],
                                              self.actions)
        self.assertEqual(self.actions['PUMP_IN'], behavior_4b)

    def test_behavior_5(self):
        """
        Test 5 - If the pump is performing PUMP_OUT and the height is below
            the target height, then the pump shall be turned to PUMP_OFF,
            otherwise, the pump shall remain at PUMP_OUT.
        """

        behavior_5a = self.new_decider.decide(99, self.actions['PUMP_OUT'],
                                              self.actions)
        self.assertEqual(self.actions['PUMP_OFF'], behavior_5a)

        behavior_5b = self.new_decider.decide(101, self.actions['PUMP_OUT'],
                                              self.actions)
        self.assertEqual(self.actions['PUMP_OUT'], behavior_5b)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        """
            Sets the necessary varialbles to test the Controller class
        """

        self.pump = Pump('127.0.0.1', 8000)
        self.pump.set_state = MagicMock(return_value=True)

        self.new_sensor = Sensor('127.0.0.1', 8000)

        self.new_decider = Decider(100, .10)

        self.new_controller = Controller(self.new_sensor, self.pump,
                                         self.new_decider)

        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

    def test_controller_tick(self):
        """
            Tests each of the behaviors defined in the Controller class
        """
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OFF)
        self.new_sensor.measure = MagicMock(return_value=89)
        self.new_decider.decide = MagicMock(return_value=self.pump.PUMP_IN)

        # 1. query the sensor for the current height of liquid in the tank

        self.assertEqual(self.new_sensor.measure(), 89)

        # 2. query the pump for its current state (pumping in,
        #    pumping out, or at rest)

        self.assertEqual(self.pump.get_state(), self.actions['PUMP_OFF'])

        # 3. query the decider for the next appropriate state of the pump,
        #    given the above
        next_state = self.new_decider.decide(self.new_sensor.measure,
                                             self.pump.get_state(),
                                             self.actions)
        self.assertEqual(next_state, self.actions['PUMP_IN'])

        # 4. set the pump to that new state
        self.assertEqual(self.new_controller.tick(), True)
