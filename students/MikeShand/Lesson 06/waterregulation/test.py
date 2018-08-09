"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from controller import Controller
from decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Decider.decide

    def test_decider(self):
        """
        Unit test for the decider class
        """
        pump = Pump('127.0.0.1', '8000')
        decider = Decider(100, 2)
        actions = {
            'PUMP_IN': pump.PUMP_IN,
            'PUMP_OUT': pump.PUMP_OUT,
            'PUMP_OFF': pump.PUMP_OFF,
        }
        high = 105
        low = 95
        sweet = 101
        self.assertEqual(1, decider.decide(low, actions["PUMP_OFF"], actions))
        self.assertEqual(-1, decider.decide(high, actions["PUMP_OFF"], actions))
        self.assertEqual(0, decider.decide(sweet, actions["PUMP_OFF"], actions))
        self.assertEqual(0, decider.decide(high, actions["PUMP_IN"], actions))
        self.assertEqual(0, decider.decide(low, actions["PUMP_OUT"], actions))
        self.assertEqual(1, decider.decide(low, actions["PUMP_IN"], actions))
        self.assertEqual(-1, decider.decide(high, actions["PUMP_OUT"], actions))

        # pump = Pump('127.0.0.1', 8000)
        # pump.set_state = MagicMock(return_value=True)

        # self.fail("Remove this test.")


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick
    def test_tick(self):

        pump = Pump('127.0.0.1', '8000')
        decider = Decider(100, 2)
        sensor = Sensor('127.0.0.1', '8000')
        controller = Controller(sensor, pump, decider)
        sensor.measure = MagicMock(return_value=102)
        pump.set_state = MagicMock(return_value=pump.PUMP_OFF)
        pump.get_state = MagicMock(return_value=pump.PUMP_OFF)
        decider.decide = MagicMock(return_value=pump.PUMP_OFF)
        controller.tick()
        sensor.measure.assert_called_with()
        pump.get_state.assert_called_with()
        decider.decide.assert_called_with(102, pump.PUMP_OFF, controller.actions)