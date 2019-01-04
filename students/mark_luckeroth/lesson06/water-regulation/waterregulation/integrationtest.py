"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def test_ctrl_decide(self):
        """
        Method tests combined function of controller and decider
        """
        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=0)
        sensor = Sensor('127.0.0.1', 8000)
        sensor.measure = MagicMock(return_value=10.)
        decider = Decider(10., 0.05)
        controller = Controller(sensor, pump, decider)

        self.assertEqual(controller.tick(), True)
        pump.set_state.assert_called_with(controller.actions['PUMP_OFF'])

        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=0)
        sensor.measure = MagicMock(return_value=1.)
        self.assertEqual(controller.tick(), True)
        pump.set_state.assert_called_with(controller.actions['PUMP_IN'])

        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=0)
        sensor.measure = MagicMock(return_value=20.)
        self.assertEqual(controller.tick(), True)
        pump.set_state.assert_called_with(controller.actions['PUMP_OUT'])

        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=1)
        sensor.measure = MagicMock(return_value=20.)
        self.assertEqual(controller.tick(), True)
        pump.set_state.assert_called_with(controller.actions['PUMP_OFF'])

        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=1)
        sensor.measure = MagicMock(return_value=1.)
        self.assertEqual(controller.tick(), True)
        pump.set_state.assert_called_with(controller.actions['PUMP_IN'])

        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=-1)
        sensor.measure = MagicMock(return_value=1.)
        self.assertEqual(controller.tick(), True)
        pump.set_state.assert_called_with(controller.actions['PUMP_OFF'])

        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=-1)
        sensor.measure = MagicMock(return_value=20.)
        self.assertEqual(controller.tick(), True)
        pump.set_state.assert_called_with(controller.actions['PUMP_OUT'])
