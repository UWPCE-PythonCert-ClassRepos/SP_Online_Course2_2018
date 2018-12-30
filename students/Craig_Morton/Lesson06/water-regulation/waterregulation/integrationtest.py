"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump as P
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def setUp(self):
        """
        Declare the sensor and pump objects for each test, and declare
        the mock for the pump's state setter method.
        """
        self.sensor = Sensor('127.0.0.1', 8000)
        self.pump = P('127.0.0.1', 8000)
        self.pump.set_state = MagicMock(return_value=True)

    def test_run_water_regulator1(self):
        """
        Run the sensor, pump, and controller against random real-life
        situations.
        """

        # Start with a controller w/target height 200, margin 20
        controller = Controller(self.sensor, self.pump, Decider(200, 0.1))

        # Begin w/a height of 250 and off state, then react accordingly
        # Decider behavior 2
        self.sensor.measure = MagicMock(return_value=250)
        self.pump.get_state = MagicMock(return_value=P.PUMP_OFF)
        controller.tick()
        self.pump.set_state.assert_called_with(controller.actions['PUMP_OUT'])

        # Decider behavior 5b
        self.sensor.measure = MagicMock(return_value=215)
        self.pump.get_state = MagicMock(return_value=P.PUMP_OUT)
        controller.tick()
        self.pump.set_state.assert_called_with(controller.actions['PUMP_OUT'])

        # Decider behavior 5a
        self.sensor.measure = MagicMock(return_value=199)
        self.pump.get_state = MagicMock(return_value=P.PUMP_OUT)
        controller.tick()
        self.pump.set_state.assert_called_with(controller.actions['PUMP_OFF'])

    def test_run_water_regulator2(self):
        """
        Run the sensor, pump, and controller against random real-life
        situations, now with a changed decider.
        """

        # Change to a controller w/target height 400, margin 32
        controller = Controller(self.sensor, self.pump, Decider(400, 0.08))

        # Decider behavior 1
        self.sensor.measure = MagicMock(return_value=199)
        self.pump.get_state = MagicMock(return_value=P.PUMP_OFF)
        controller.tick()
        self.pump.set_state.assert_called_with(controller.actions['PUMP_IN'])

        # Decider behavior 4b
        self.sensor.measure = MagicMock(return_value=380)
        self.pump.get_state = MagicMock(return_value=P.PUMP_IN)
        controller.tick()
        self.pump.set_state.assert_called_with(controller.actions['PUMP_IN'])

        # Decider behavior 4a
        self.sensor.measure = MagicMock(return_value=401)
        self.pump.get_state = MagicMock(return_value=P.PUMP_IN)
        controller.tick()
        self.pump.set_state.assert_called_with(controller.actions['PUMP_OFF'])

        # Decider behavior 3
        self.sensor.measure = MagicMock(return_value=401)
        self.pump.get_state = MagicMock(return_value=P.PUMP_OFF)
        controller.tick()
        self.pump.set_state.assert_called_with(controller.actions['PUMP_OFF'])
