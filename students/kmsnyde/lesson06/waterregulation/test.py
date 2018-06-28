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

    def test_decider(self):
        """"test decider.py"""

        target = 100
        margin = .05

        case1 = Decider(target, margin)

        high = 107
        within = 97
        low = 94

        actions = {
            'PUMP_IN': 1,
            'PUMP_OUT': -1,
            'PUMP_OFF': 0}

        self.assertEqual(1, case1.decide(low, actions['PUMP_OFF'], actions))
        self.assertEqual(-1, case1.decide(high, actions['PUMP_OFF'], actions))
        self.assertEqual(0, case1.decide(within, actions['PUMP_OFF'], actions))
        self.assertEqual(0, case1.decide(101, actions['PUMP_IN'], actions))
        self.assertEqual(1, case1.decide(100, actions['PUMP_IN'], actions))
        self.assertEqual(0, case1.decide(90, actions['PUMP_OUT'], actions))
        self.assertEqual(-1, case1.decide(101, actions['PUMP_OUT'], actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    sensor = Sensor('127.0.0.1', '8000')
    pump = Pump('127.0.0.1', '8000')
    dec = Decider(100, .05)
    con = Controller(sensor, pump, dec)

    def test_controller_tick(self):
        """test the tick function in the controller"""

        self.con.tick()

        # liquid height
        self.sensor.measure = MagicMock(return_value=100)
        self.sensor.measure.assert_called_with()

        # state of pump
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_IN)
        self.pump.get_state.assert_called_with()

        # decider next state for pump
        self.dec.decide = MagicMock(return_value=self.pump.PUMP_IN)
        self.dec.decide.assert_called_with(94, self.pump.PUMP_OFF,
                                           self.controller.actions)
