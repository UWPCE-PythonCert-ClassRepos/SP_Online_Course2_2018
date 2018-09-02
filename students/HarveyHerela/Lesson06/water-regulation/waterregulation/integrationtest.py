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

    @classmethod
    def setUpClass(cls):
        # Create a controller and decider, and all the things they need
        cls.pump = Pump('127.0.0.1', 8000)
        cls.sensor = Sensor('127.0.0.1', 8000)
        cls.decider = Decider(5, 0.1)
        cls.controller = Controller(cls.sensor, cls.pump, cls.decider)

        # Now mock a few items
        cls.pump.get_state = MagicMock(return_value='PUMP_OFF')
        cls.pump.set_state = MagicMock(return_value=True)

    def test_fill_to_height(self):
        """Tests filling up the tank"""
        self.sensor.measure = MagicMock(side_effect=[
            0, 1, 2, 3, 4, 5, 6, 7, 8])

        # Now fill it up
        for i in range(5):
            self.controller.tick()
            self.pump.set_state.assert_called_with(Pump.PUMP_IN)

        # Tank is full, make sure the pump is commanded off
        self.controller.tick()
        self.pump.set_state.assert_called_with(Pump.PUMP_OFF)

    def test_drain_to_height(self):
        """Tests draining the tank to the level"""
        self.sensor.measure = MagicMock(side_effect=[
            10, 9, 8, 7, 6, 5, 4, 3, 2, 1])

        # Now drain it
        for i in range(5):
            self.controller.tick()
            self.pump.set_state.assert_called_with(Pump.PUMP_OUT)

        # Tank is full, make sure the pump is commanded off
        self.controller.tick()
        self.pump.set_state.assert_called_with(Pump.PUMP_OFF)
