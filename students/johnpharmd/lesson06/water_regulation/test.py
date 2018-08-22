"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from waterregulation.controller import Controller
from waterregulation.decider import Decider


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

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick

    def setUp(self):
        self.sensor = Sensor('127.0.0.1', 514)
        self.pump = Pump('127.0.0.1', 8000)
        self.decider = Decider(10, 0.05)

        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_sensor_call(self):
        self.sensor.measure = MagicMock(return_value=0)

        self.controller.tick()
