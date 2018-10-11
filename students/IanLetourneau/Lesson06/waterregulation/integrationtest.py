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

    def test_all_modules(self):
        """Function to test all modules in combination"""
        pump = Pump('127.0.0.1', 8000)
        sensor = Sensor('127.0.0.1', 8000)
        decider = Decider(50, .05)
        controller = Controller(sensor, pump, decider)

        controller.pump.set_state = MagicMock(return_value=True)
        controller.sensor.measure = MagicMock(return_value=60)
        controller.pump.get_state = MagicMock(return_value=decider.decide(
            60, controller.actions['PUMP_OFF'], controller.actions))
        controller.tick()
