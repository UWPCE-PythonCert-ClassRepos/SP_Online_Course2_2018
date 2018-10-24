"""
AUTHOR: Micah Braun
PROJECT NAME: test_run.py (for waterregulation modules)
DATE CREATED: 10/19/2018
UPDATED: 10/22/2018
PURPOSE: Lesson 6
DESCRIPTION: Unittests for Pump, Sensor, Controller,
and Decider classes and their modules to check for
proper functionality.
"""
import unittest
from unittest.mock import MagicMock
from pump import Pump
from sensor import Sensor
from controller import Controller
from decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for Decider class
    """
    def setUp(self):
        self.actions = {'PUMP_IN': 1,
                        'PUMP_OFF': 0,
                        'PUMP_OUT': -1
                        }

    def test_decide(self):
        """
        Test decide method of Decider class:
        P1: If PUMP_OFF, and levels are below margin,
        decider.decide should choose to PUMP_IN
        P2: If PUMP_OFF, and levels are higher than
        margin, decider.decide should choose to
        PUMP_OUT
        P3: If PUMP_OFF and levels are within margin,
        decider.decide should keep pump at PUMP_OFF
        P4a: If pump is set to PUMP_IN and levels
        exceed margin tolerance, decider.decide should
        set pump to PUMP_OFF
        P4b: If pump is set to PUMP_IN and levels
        do not exceed margin tolerance, decider.decide
        should not change state
        P5a: If pump is set to PUMP_OUT and levels drop
        below margin, decider.decide should set pump to
        PUMP_OFF
        P5b: If pump is set to PUMP_OUT and levels are
        above margin, pump should not change state
        """

        decider = Decider(100, .10)

        self.assertEqual(1, decider.decide(88, 0, self.actions))        # /P1
        self.assertEqual(-1, decider.decide(120, 0, self.actions))      # /P2
        self.assertEqual(0, decider.decide(101, 0, self.actions))       # /P3
        self.assertEqual(0, decider.decide(111, 1, self.actions))       # /P4a
        self.assertEqual(1, decider.decide(100, 1, self.actions))       # /P4b
        self.assertEqual(0, decider.decide(89, -1, self.actions))       # /P5a
        self.assertEqual(-1, decider.decide(111, -1, self.actions))     # /P5b


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """
    def setUp(self):
        """
        Set up method for test_controller
        """
        self.sensor = Sensor('127.0.0.1', 8000)
        self.sensor.measure = MagicMock(return_value=100)
        self.pump = Pump('127.0.0.1', 8000)
        self.pump.set_state = MagicMock(return_value=True)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OFF)
        self.decider = Decider(100, .10)
        self.decider.decide = MagicMock(return_value=self.pump.PUMP_OFF)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.controller.tick()

        self.actions = {'PUMP_IN': self.pump.PUMP_IN,
                        'PUMP_OUT': self.pump.PUMP_OUT,
                        'PUMP_OFF': self.pump.PUMP_OFF
                        }

    def test_controller(self):
        """
        Test controller and tick:
        1: Check sensor.measure for accuracy
        2: test pump.get_state for correct return
        3: decider.decide for correct 'decision'
        4: Test pump.set_state for expected mocked output
        5: Test sensor.measure return val is correct type
        6: Round-a-bout way of testing the try/except
        block of controller.tick() -- if pump.set_state
        returns False, it is because of a TypeError,
        checking that if it is False, it raises TypeError
        """
        self.assertEqual(100, self.sensor.measure())            # 1
        self.assertEqual(0, self.pump.get_state())              # 2
        self.assertEqual(0, self.decider.decide(100,
                         0, self.actions))                      # 3
        self.assertEqual(True, self.pump.set_state
                         (self.actions['PUMP_OFF']))            # 4
        self.assertTrue(self.sensor.measure() == float(100))    # 5
        if self.pump.set_state(False):                          # 6
            self.assertRaises(TypeError)
