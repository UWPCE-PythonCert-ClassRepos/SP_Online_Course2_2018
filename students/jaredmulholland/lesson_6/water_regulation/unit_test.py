"""
Unit tests for the water-regulation module
"""

from unittest import TestCase
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from waterregulation.controller import Controller
from waterregulation.decider import Decider

class DeciderTests(TestCase):
    """
    Unit tests for the Decider class
    """

    def setup(self):
        """
        Create sensor, pump, decider and controller
        """
        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1', 8000)
        self.decider = Decider(100, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

        self.actions = {'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1}

    def test_decider_condition_1(self):
        """tests:
        If the pump is off and the height is below the margin region, then the
        pump should be turned to PUMP_IN.
        """
        self.assertEqual(self.decider.decide(80, self.pump.PUMP_OFF, self.controller.actions),
                         self.controller.actions['PUMP_IN'])


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
