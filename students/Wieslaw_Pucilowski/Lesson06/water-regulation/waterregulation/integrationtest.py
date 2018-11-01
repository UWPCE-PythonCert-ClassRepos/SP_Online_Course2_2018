"""
Module tests for the water-regulation module
"""
__author__ = "Wieslaw Pucilowski"

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module.
    3 test methods define. Each sets limits for MagicMock
    used inside the method.
    """

    def setUp(self):
        """
        Setup for all 3 tests
        """
        self.pump = Pump('127.0.0.1', '8080')
        self.sensor = Sensor('127.0.0.1', '8081')
        self.decider = Decider(100, .10)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_app_1(self):
        """
        Testing the app 1
        :return:
        """
        self.controller.pump.set_state = MagicMock(return_value=True)
        self.controller.decider.decide = MagicMock(return_value=True)
        for action in self.controller.actions.values():
            for level in range(50, 150, 10):
                self.controller.sensor.measure = MagicMock(return_value=level)
                self.controller.pump.get_state = MagicMock(return_value=action)
                self.controller.tick()
                # print("test 3:", level, action, self.controller.actions)
                self.controller.decider.decide\
                    .assert_called_with(level, action, self.controller.actions)

    def test_app_2(self):
        """
        Testing the app 2
        :return:
        """
        # initial pump state:
        pump_state = self.controller.actions['PUMP_IN']
        # print(pump_state)
        self.controller.pump.set_state = MagicMock(return_value=True)
        print("1", pump_state)
        for level in range(50, 150, 10):
            self.controller.sensor.measure = MagicMock(return_value=level)
            self.controller.pump.get_state = MagicMock(return_value=pump_state)
            pump_state =\
                self.controller.decider.decide(level,
                                               pump_state,
                                               self.controller.actions)
            self.controller.tick()
            # print("Test 1", pump_state , level)
            self.controller.pump.set_state.assert_called_with(pump_state)

    def test_app_3(self):
        """
        Testing the app 3
        :return:
        """

        self.controller.sensor.measure = MagicMock(return_value=90)
        self.controller.pump.get_state =\
            MagicMock(return_value=self.controller.actions['PUMP_IN'])
        self.controller.pump.set_state = MagicMock(return_value=True)

        self.controller.pump.set_state = MagicMock(return_value=True)
        for action in self.controller.actions.values():
            for level in range(50, 150, 10):
                self.controller.sensor.measure = MagicMock(return_value=level)
                self.controller.pump.get_state = MagicMock(return_value=action)
                self.controller.tick()
                new = self.controller.decider.\
                    decide(level, action, self.controller.actions)
                # print("test 2:", new)
                self.controller.pump.set_state.assert_called_with(new)
