"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock
from pump import Pump
from sensor import Sensor
from .decider import Decider
from .controller import Controller


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    # test each of the behaviors defined for
    # Decider.decide

    def test_below_margin(self):
        """ test each state of decider
        """

        pump = Pump('127.0.0', 8000)
        actions = {
            'PUMP_IN': pump.PUMP_IN,
            'PUMP_OUT': pump.PUMP_OUT,
            'PUMP_OFF': pump.PUMP_OFF,
        }
        decider = Decider(100, 0.1)
        state = decider.decide(89, Pump.PUMP_OFF, actions)
        self.assertEqual(state, Pump.PUMP_IN)
        state = decider.decide(111, Pump.PUMP_OFF, actions)
        self.assertEqual(state, Pump.PUMP_OUT)
        state = decider.decide(100, Pump.PUMP_OFF, actions)
        self.assertEqual(state, Pump.PUMP_OFF)
        state = decider.decide(150, Pump.PUMP_IN, actions)
        self.assertEqual(state, Pump.PUMP_OFF)
        state = decider.decide(80, Pump.PUMP_IN, actions)
        self.assertEqual(state, Pump.PUMP_IN)
        state = decider.decide(80, Pump.PUMP_OUT, actions)
        self.assertEqual(state, Pump.PUMP_OFF)


class ControllerTests(unittest.TestCase):
    """
    test case for each of the behaviors defined for Controller.tick
    """

    def test_tick(self):
        """
        test case to test tick method
        """

        pump = Pump('127.0.0', 8000)
        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=Pump.PUMP_OFF)
        sensor = Sensor('127.0.0', 8000)
        sensor.measure = MagicMock(return_value=89)
        decider = Decider(100, 0.1)
        controller = Controller(sensor, pump, decider)
        self.assertEqual(Pump.PUMP_IN, controller.tick())
