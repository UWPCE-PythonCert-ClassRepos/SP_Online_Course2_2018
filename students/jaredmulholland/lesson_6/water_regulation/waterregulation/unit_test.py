"""
Unit tests for the water-regulation module
"""
from unittest import TestCase
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class DeciderTests(TestCase):
    """
    Unit tests for the Decider class
    """
    @classmethod
    def setup(cls):
        """
        Create sensor, pump, decider and controller
        """
        cls.pump = Pump('127.0.0.1', 8000)
        cls.decider = Decider(100, 0.05)
        cls.actions = {'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1}

    def test_decider_condition_1(self):
        """tests:
        If the pump is off and the height is below the margin region, then the
        pump should be turned to PUMP_IN.
        """
        self.assertEqual(self.decider.decide(80, self.pump.PUMP_OFF, self.actions),
                         self.actions['PUMP_IN'])

    def test_decider_condition_2(self):
        """test:
        If the pump is off and the height is above the margin region,
        then the pump should be turned to PUMP_OUT
        """
        self.assertEqual(self.decider.decide(120, self.pump.PUMP_OFF, self.actions),
                         self.actions['PUMP_OUT'])

    def test_decider_condition_3(self):
        """test:
        If the pump is off and the height is within the margin region,
        or the exact boundary of the margin region, the the pump shall
        remain at PUMP_OFF
        """
        self.assertEqual(self.decider.decide(100, self.pump.PUMP_OFF, self.actions),
                         self.actions['PUMP_OUT'])

    def test_decider_condition_4(self):
        """test:
        If the pump is performing PUMP_IN and the height is above the target
        height, then the pump shall be turned ot PUMP_OFF, otherwise, the
        pump shall remain at PUMP_IN
        """

        self.assertEqual(self.decider.decide(120, self.pump.PUMP_IN, self.actions),
                         self.actions['PUMP_OFF'])

        self.assertEqual(self.decider.decide(94, self.pump.PUMP_IN, self.actions),
                         self.actions['PUMP_IN'])

    def test_decider_condition_5(self):
        """test:
        If the pump is performing PUMP_OUT and the height is below the target
        height, then the pump shall be turned to PUMP_OFF, otherwise, the
        pump shall remain at PUMP_OUT
        """

        self.assertEqual(self.decider.decide(90, self.pump.PUMP_OUT, self.actions),
                         self.actions['PUMP_OFF'])

        self.assertEqual(self.decider.decide(106, self.pump.PUMP_OUT, self.actions),
                         self.actions['PUMP_OUT'])


class ControllerTests(TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):

        self.pump = Pump('127.0.0.1', 8000)
        self.pump.set_state = MagicMock(return_value=True)
        self.pump.get_state = MagicMock(return_value=self.pump.PUMP_IN)

        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

        self.sensor = Sensor('127.0.0.1', 8000)
        self.sensor.measure = MagicMock(return_value=75)

        self.decider = Decider(100, .05)
        self.decider.decide = MagicMock(return_value=self.pump.PUMP_IN)

        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_controller(self):
        """Test the controller functionality"""

        self.assertEqual(self.controller.tick(), True)
        pump_in = self.pump.PUMP_IN
        self.decider.decide.assert_called_with(current_height=75, current_action=pump_in, actions=self.actions)
