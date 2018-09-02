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

    DUMMY_ADDR = '127.0.0.1'
    DUMMY_PORT = '8000'

    def test_tick(self):
        """Test logic of sensor, pump."""
        sensor = Sensor(ModuleTests.DUMMY_ADDR, ModuleTests.DUMMY_PORT)
        sensor.measure = MagicMock(return_value=10)
        pump = Pump(ModuleTests.DUMMY_ADDR, ModuleTests.DUMMY_PORT)
        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=Pump.PUMP_IN)
        decider = Decider(10, 0.05)
        decider.decide = MagicMock(return_value=100)

        controller = Controller(sensor, pump, decider)
        controller.tick()

        sensor.measure.assert_called_once_with()
        pump.get_state.assert_called_once_with()
        pump.set_state.assert_called_once_with(100)
