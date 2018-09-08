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

        pump = Pump(ModuleTests.DUMMY_ADDR, ModuleTests.DUMMY_PORT)
        pump.set_state = MagicMock(return_value=True)

        sensor = Sensor(ModuleTests.DUMMY_ADDR, ModuleTests.DUMMY_PORT)

        decider = Decider(10, 0.1)
        pump.get_state = MagicMock(return_value=Pump.PUMP_OFF)

        controller = Controller(sensor, pump, decider)

        test_sequence = [
            {'measure': 0.0, 'next_state': controller.actions['PUMP_IN']},
            {'measure': 4.0, 'next_state': controller.actions['PUMP_IN']},
            {'measure': 8.0, 'next_state': controller.actions['PUMP_IN']},
            {'measure': 9.0, 'next_state': controller.actions['PUMP_IN']},
            {'measure': 10.0, 'next_state': controller.actions['PUMP_IN']},
            {'measure': 11.0, 'next_state': controller.actions['PUMP_OFF']},
            {'measure': 11.1, 'next_state': controller.actions['PUMP_OUT']},
            {'measure': 12.0, 'next_state': controller.actions['PUMP_OUT']},
            {'measure': 11.1, 'next_state': controller.actions['PUMP_OUT']},
            {'measure': 10.0, 'next_state': controller.actions['PUMP_OUT']},
            {'measure': 9.9, 'next_state': controller.actions['PUMP_OFF']},
        ]

        for test in test_sequence:
            # Inject height
            sensor.measure = MagicMock(return_value=test['measure'])

            # Do a tick
            controller.tick()

            # Check that pump.set_state() got called with the correct state
            pump.set_state.assert_called_with(test['next_state'])

            # Update pump.get_state() to return the next expected state
            pump.get_state = MagicMock(return_value=test['next_state'])
