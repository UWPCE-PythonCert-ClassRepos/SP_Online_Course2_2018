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

    def test_decider_controller_integration(self):
        """
        Method that tests and ensures that the decider and controller work
        well together
        """

        pump = Pump('0.0.0.1', 541)
        sensor = Sensor('0.0.0.1', 541)
        decider = Decider(85, .05)
        controller = Controller(sensor, pump, decider)
        sensor.measure = MagicMock(return_value=60)
        pump.get_state = MagicMock(return_value=1)
        pump.set_state = MagicMock(return_value=True)
        result = decider.decide(65, 0, controller.actions)

        controller.tick()

        self.assertEqual(result, 1)
