"""
Unit tests for waterregulation
"""
import unittest
from unittest.mock import MagicMock
import sys

sys.path.insert(0, '../pump')
sys.path.insert(0, '../sensor')

from pump import Pump
from sensor import Sensor

from controller import Controller
from decider import Decider

actions = {
    'PUMP_IN': 1,
    'PUMP_OFF': 0,
    'PUMP_OUT': -1
}

class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def test_decider_decide(self):
        """
        Test the decide method
        """

        decider = Decider(1000.0, 0.5)
        
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
        Testing the tick method in controller
        :return:
        """
        pump_address = Pump('127.0.0.1', 8000)
        sensor_address = Sensor('127.0.0.1', 8000)
        decider_vals = Decider(100, .10)
        controller_all = Controller(sensor_address, pump_address, decider_vals)
        sensor_address.measure = MagicMock(return_value=95)
        pump_address.get_state = MagicMock(return_value=pump_address.PUMP_IN)
        decider_vals.decide = MagicMock(return_value=pump_address.PUMP_IN)
        pump_address.set_state = MagicMock(return_value=True)
        controller_all.tick()
        sensor_address.measure.assert_called_with()
        pump_address.get_state.assert_called_with()
        decider_vals.decide.assert_called_with(
            95, pump_address.PUMP_IN, actions)
