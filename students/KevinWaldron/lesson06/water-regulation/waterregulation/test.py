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

    def test_decide(self):
        """
        Test the decide method
        """
        decider = Decider(1000.0, 0.5)

        actions = {
            'PUMP_IN': Pump.PUMP_IN,
            'PUMP_OUT': Pump.PUMP_OUT,
            'PUMP_OFF': Pump.PUMP_OFF,
        }

        result = decider.decide(200, Pump.PUMP_OFF, actions)
        self.assertEqual(result, Pump.PUMP_IN)
        result = decider.decide(2000, Pump.PUMP_OFF, actions)
        self.assertEqual(result, Pump.PUMP_OUT)
        result = decider.decide(500, Pump.PUMP_OFF, actions)
        self.assertEqual(result, Pump.PUMP_OFF)
        result = decider.decide(1001, Pump.PUMP_IN, actions)
        self.assertEqual(result, Pump.PUMP_OFF)
        result = decider.decide(999, Pump.PUMP_IN, actions)
        self.assertEqual(result, Pump.PUMP_IN)
        result = decider.decide(999, Pump.PUMP_OUT, actions)
        self.assertEqual(result, Pump.PUMP_OFF)
        result = decider.decide(1001, Pump.PUMP_OUT, actions)
        self.assertEqual(result, Pump.PUMP_OUT)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick(self):
        """
        Test the tick method
        """
        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=Pump.PUMP_OUT)

        sensor = Sensor('127.0.0.1', 8000)
        sensor.measure = MagicMock(return_value=1.0)

        decider = Decider(1000.0, 0.5)

        controller = Controller(sensor, pump, decider)

        self.assertTrue(controller.tick())
