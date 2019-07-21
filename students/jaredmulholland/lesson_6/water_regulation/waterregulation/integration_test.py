"""
Module tests for the water-regulation module
"""

from unittest import TestCase
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class ModuleTests(TestCase):
    """
    Module tests for the water-regulation module
    """
    def setUpClass(self):
        """setting up for controller test"""
        self.pump = Pump('127.0.0.1', 8000)
        self.sensor = Sensor('127.0.0.1', 8000)
        self.decider = Decider(100, 0.05)

        self.actions = {'PUMP_IN': 1, 'PUMP_OFF': 0, 'PUMP_OUT': -1}

        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_integration(self):
        """test integration of controller"""

        self.sensor.measure = MagicMock(return_value=80)
        self.pump.get_state = MagicMock(return_value=self.actions['PUMP_IN'])

        tick_ = self.controller.tick()

        self.assertEqual(tick_, True)
