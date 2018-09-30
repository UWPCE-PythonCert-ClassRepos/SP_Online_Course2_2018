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

    def setUp(self):
        self.actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1
        }

    def test_decide(self):
        """ Test decide method of Decider class """
        decider = Decider(50, .05)
        # 1
        self.assertEqual(1, decider.decide(47, 0, self.actions))
        # 2
        self.assertEqual(-1, decider.decide(53, 0, self.actions))
        # 3
        self.assertEqual(0, decider.decide(50, 0, self.actions))
        # 4
        self.assertEqual(0, decider.decide(53, 1, self.actions))
        self.assertEqual(1, decider.decide(50, 1, self.actions))
        # 5
        self.assertEqual(0, decider.decide(47, -1, self.actions))
        self.assertEqual(-1, decider.decide(53, -1, self.actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        # sensor
        self.sensor = Sensor('127.0.0.1', 8000)
        self.sensor.measure = MagicMock(return_value=50)

        # pump
        self.pump = Pump('127.0.0.1', 8000)
        self.pump.set_state = MagicMock(return_value=True)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OFF)

        # decider
        self.decider = Decider(50, .05)
        self.decider.decide = MagicMock(return_value=self.pump.PUMP_OFF)

        # controller
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.controller.tick()

        # actions
        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

    def test_controller(self):
        """
        Test controller and tick
        """

        # measure
        self.sensor.measure.assert_called_with()
        self.assertEqual(50, self.sensor.measure())

        # get state
        self.pump.get_state.assert_called_with()
        self.assertEqual(0, self.pump.get_state())

        # decide
        self.decider.decide.assert_called_with(
            50, self.actions['PUMP_OFF'], self.actions
        )
        self.assertEqual(0, self.decider.decide(50, 0, self.actions))

        # set state
        self.pump.set_state.assert_called_with(self.actions['PUMP_OFF'])
        self.assertEqual(True, self.pump.set_state(self.actions['PUMP_OFF']))
