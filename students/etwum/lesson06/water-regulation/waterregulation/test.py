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

    #       Decider.decide

    def test_decide(self):

        actions = {'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1}

        target = Decider(100, .05)

        self.assertEqual(1, target.decide(94, actions['PUMP_OFF'], actions))
        self.assertEqual(-1, target.decide(106, actions['PUMP_OFF'], actions))
        self.assertEqual(0, target.decide(104, actions['PUMP_OFF'], actions))
        self.assertEqual(0, target.decide(106, actions['PUMP_IN'], actions))
        self.assertEqual(1, target.decide(93, actions['PUMP_IN'], actions))
        self.assertEqual(0, target.decide(93, actions['PUMP_OUT'], actions))
        self.assertEqual(-1, target.decide(112, actions['PUMP_OUT'], actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """
    #       Controller.tick

    def setUp(self):
        """
        Sets up controller.
        """
        self.sensor = Sensor("127.0.0.1", 8080)
        self.pump = Pump("127.0.0.1", 8050)
        self.decider = Decider(100, .05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_tick(self):
        self.sensor.measure = MagicMock(return_value=95)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_IN)
        self.decider.decide = MagicMock(return_value=self.pump.PUMP_IN)
        self.pump.set_state = MagicMock(return_value=True)
        self.controller.tick()

        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.decider.decide.assert_called_with(95, self.pump.PUMP_IN,
                                               self.controller.actions)
        self.pump.set_state.assert_called_with(self.pump.PUMP_IN)
