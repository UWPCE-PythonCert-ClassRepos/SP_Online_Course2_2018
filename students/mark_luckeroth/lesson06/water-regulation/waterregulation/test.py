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

    def test_decide(self):
        """
        Method to test decide function
        """
        pump = Pump('127.0.0.1', 8000)
        sensor = Sensor('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)
        decider = Decider(10., 0.05)
        controller = Controller(sensor, pump, decider)

        self.assertEqual(decider.decide(1.0, int(0), controller.actions),
                         controller.actions['PUMP_IN'])
        self.assertEqual(decider.decide(20.0, int(0), controller.actions),
                         controller.actions['PUMP_OUT'])
        self.assertEqual(decider.decide(10.0, int(0), controller.actions),
                         controller.actions['PUMP_OFF'])
        self.assertEqual(decider.decide(20.0, int(1), controller.actions),
                         controller.actions['PUMP_OFF'])
        self.assertEqual(decider.decide(1.0, int(1), controller.actions),
                         controller.actions['PUMP_IN'])
        self.assertEqual(decider.decide(1.0, int(-1), controller.actions),
                         controller.actions['PUMP_OFF'])
        self.assertEqual(decider.decide(20.0, int(-1), controller.actions),
                         controller.actions['PUMP_OUT'])
        with self.assertRaises(ValueError):
            decider.decide(10., 2.5, controller.actions)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_control(self):
        """
        Method to test function of control method
        """
        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=0)
        sensor = Sensor('127.0.0.1', 8000)
        sensor.measure = MagicMock(return_value=10.)
        decider = Decider(10., 0.05)
        decider.decide = MagicMock(return_value=True)
        controller = Controller(sensor, pump, decider)

        self.assertEqual(controller.tick(), True)
