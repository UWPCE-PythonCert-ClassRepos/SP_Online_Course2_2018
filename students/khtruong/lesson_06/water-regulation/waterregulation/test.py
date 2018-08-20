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
    def test_actions(self):
        """
        Just some example syntax that you might use
        """
        actions = {
            'PUMP_IN': Pump.PUMP_IN,
            'PUMP_OUT': Pump.PUMP_OUT,
            'PUMP_OFF': Pump.PUMP_OFF
            }

        pump_off = Pump.PUMP_OFF
        pump_in = Pump.PUMP_IN
        pump_out = Pump.PUMP_OUT
        target = 100
        margin = 0.05
        above = 106
        below = 94
        meet = 100

        decider = Decider(target, margin)
        self.assertEqual(decider.decide(below, pump_off, actions), pump_in)
        self.assertEqual(decider.decide(above, pump_off, actions), pump_out)
        self.assertEqual(decider.decide(meet, pump_off, actions), pump_off)
        self.assertEqual(decider.decide(above, pump_in, actions), pump_off)
        self.assertEqual(decider.decide(below, pump_in, actions), pump_in)
        self.assertEqual(decider.decide(meet, pump_in, actions), pump_in)
        self.assertEqual(decider.decide(above, pump_out, actions), pump_out)
        self.assertEqual(decider.decide(below, pump_out, actions), pump_off)
        self.assertEqual(decider.decide(meet, pump_out, actions), pump_out)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        """Setup docstring."""
        address = "127.0.0.1"
        port = "8000"
        self.sensor = Sensor(address, port)
        self.pump = Pump(address, port)
        self.decider = Decider(100, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def tearDown(self):
        """Teardown docstring."""
        pass

    def test_tick(self):
        """Method docstring."""
        self.sensor.measure = MagicMock(return_value=90)
        self.pump.get_state = MagicMock(return_value=Pump.PUMP_OFF)
        self.decider.decide = MagicMock(return_value=Pump.PUMP_IN)
        self.pump.set_state = MagicMock(return_value=True)
        self.controller.tick()
        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.decider.decide.assert_called_with(90, self.pump.PUMP_OFF,
                                               self.controller.actions)
        self.pump.set_state.assert_called_with(self.pump.PUMP_IN)
