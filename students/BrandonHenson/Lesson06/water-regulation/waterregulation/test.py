"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider

Actions = {
    'PUMP_IN': 1,
    'PUMP_OFF': 0,
    'PUMP_OUT': -1
}


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Decider.decide

    def test_decider_decide(self):
        """
        Unit test for decider
        :return:
        """

        deciders = Decider(100, .10)
        decide1 = deciders.decide(85, Actions['PUMP_OFF'], Actions)
        decide2 = deciders.decide(115, Actions['PUMP_OFF'], Actions)
        decide3 = deciders.decide(105, Actions['PUMP_OFF'], Actions)
        decide4 = deciders.decide(105, Actions['PUMP_IN'], Actions)
        decide5 = deciders.decide(95, Actions['PUMP_IN'], Actions)
        decide6 = deciders.decide(95, Actions['PUMP_OUT'], Actions)
        decide7 = deciders.decide(105, Actions['PUMP_OUT'], Actions)
        self.assertEqual(Actions['PUMP_IN'], decide1)
        self.assertEqual(Actions['PUMP_OUT'], decide2)
        self.assertEqual(Actions['PUMP_OFF'], decide3)
        self.assertEqual(Actions['PUMP_OFF'], decide4)
        self.assertEqual(Actions['PUMP_IN'], decide5)
        self.assertEqual(Actions['PUMP_OFF'], decide6)
        self.assertEqual(Actions['PUMP_OUT'], decide7)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick
    def test_tick(self):
        """
        Testing the tick method in controller
        :return:
        """
        pump_address = Pump('127.0.0.1', 8080)
        sensor_address = Sensor('127.0.0.1', 8083)
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
            95, pump_address.PUMP_IN, Actions)
