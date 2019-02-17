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

    # TODO: write a test or tests for each of the behaviors defined for
    #       Decider.decide

    def test_dummy(self):
        """
        Just some example syntax that you might use
        """

        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)

        self.fail("Remove this test.")


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        self.sensor = Sensor('127.0.0.1', 8000)
        self.pump = Pump('127.0.0.1', 8000)
        self.decider = Decider('127.0.0.1', 8000)

        self.controller = Controller(sensor=self.sensor,
                                     pump=self.pump,
                                     decider=self.decider)

    def test_measure_is_called(self):
        """given controller with sensor attached
        when get_measurement is called, the sensor measure method
        gets called"""
        self.sensor.measure = MagicMock(return_value=0)

        self.controller.get_measurement()
        self.sensor.measure.assert_called_with()

    def test_get_pump_state_called(self):
        """given controoler with pump
        when controller get_pump_state called
        the pump method get_state gets called"""
        self.pump.get_state = MagicMock(return_value=0)

        self.controller.get_pump_state()
        self.pump.get_state.assert_called_with()

    def test_decider_gets_called(self):
        """given a controller
        when decide_pump_state gets called
        decider method decide gets called with inputs
        for current fluid height and pump state"""
        self.decider.decide = MagicMock(return_value=0)

        self.controller.decide_pump_state(current_height=5, 
                                          pump_state=0, 
                                          actions=self.controller.actions)
        self.decider.decide.assert_called_with(current_height=5, 
                                               pump_state=0, 
                                               actions=self.controller.actions)

    def test_controller_calls_set_pump_state(self):
        """given a controller
        when decider decides to set pump state and calls set_pump_state
        the pump set_state method is called"""
        pass

    def test_dummy(self):
        """
        Just some example syntax that you might use
        """

        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)

        self.fail("Remove this test.")
