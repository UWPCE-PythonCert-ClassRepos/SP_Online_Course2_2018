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

    def test_module(self):
        '''an integration test that combines controller and decider,
           using a MOCKED sensor and pump'''

        controller = Controller(Sensor('127.0.0.1', 8000),
                                Pump('127.0.0.1', 8000), Decider(10, 0.05))

        controller.sensor.measure = MagicMock(return_value=8)
        controller.pump.get_state = MagicMock(return_value="PUMP_OFF")
        controller.pump.set_state = MagicMock(return_value=True)

        value = controller.tick()

        self.assertEqual(value, True)

        controller.sensor.measure = MagicMock(return_value=12)
        controller.pump.get_state = MagicMock(return_value="PUMP_IN")
        controller.pump.set_state = MagicMock(return_value=True)
        value2 = controller.tick()

        self.assertEqual(value2, True)
