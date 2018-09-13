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
        """
        Create the sensor, pump, decider, and controller. The sensor is
        not really needed, and the pump isn't either except for its
        constants. The decider specifies the target height and the
        margin, while the controller is mainly needed for its constants
        (captured in a dict) as well.
        """
        self.sensor = Sensor('127.0.0.1', 8000)
        self.pump = Pump('127.0.0.1', 8000)
        self.decider = Decider(100, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    # !!Decider.decide tests below!!
    def test_decide_off_and_low(self):
        """Check correct decision if pump is off and water is low."""
        args = (90, self.pump.PUMP_OFF, self.controller.actions)
        self.assertEqual(self.decider.decide(*args),
                         self.controller.actions['PUMP_IN'])

    def test_decide_off_and_high(self):
        """Check correct decision if pump is off and water is high."""
        args = (110, self.pump.PUMP_OFF, self.controller.actions)
        self.assertEqual(self.decider.decide(*args),
                         self.controller.actions['PUMP_OUT'])

    def test_decide_off_and_medium1(self):
        """
        Check correct decision if pump is off and water is within margin
        (test 1).
        """
        args = (95, self.pump.PUMP_OFF, self.controller.actions)
        self.assertEqual(self.decider.decide(*args),
                         self.controller.actions['PUMP_OFF'])

    def test_decide_off_and_medium2(self):
        """
        Check correct decision if pump is off and water is within margin
        (test 2).
        """
        args = (100, self.pump.PUMP_OFF, self.controller.actions)
        self.assertEqual(self.decider.decide(*args),
                         self.controller.actions['PUMP_OFF'])

    def test_decide_off_and_medium3(self):
        """
        Check correct decision if pump is off and water is within margin
        (test 3).
        """
        args = (105, self.pump.PUMP_OFF, self.controller.actions)
        self.assertEqual(self.decider.decide(*args),
                         self.controller.actions['PUMP_OFF'])

    def test_decide_in_and_low(self):
        """Check correct decision if pumping in while water is low."""
        args = (90, self.pump.PUMP_IN, self.controller.actions)
        self.assertEqual(self.decider.decide(*args),
                         self.controller.actions['PUMP_IN'])

    def test_decide_in_and_high(self):
        """Check correct decision if pumping in while water is high."""
        args = (110, self.pump.PUMP_IN, self.controller.actions)
        self.assertEqual(self.decider.decide(*args),
                         self.controller.actions['PUMP_OFF'])

    def test_decide_out_and_low(self):
        """Check correct decision if pumping out while water is low."""
        args = (90, self.pump.PUMP_OUT, self.controller.actions)
        self.assertEqual(self.decider.decide(*args),
                         self.controller.actions['PUMP_OFF'])

    def test_decide_out_and_high(self):
        """Check correct decision if pumping out while water is high."""
        args = (110, self.pump.PUMP_OUT, self.controller.actions)
        self.assertEqual(self.decider.decide(*args),
                         self.controller.actions['PUMP_OUT'])


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        """
        Create the sensor, pump, decider, and controller. The sensor is
        not really needed, and the pump isn't either except for its
        constants. The decider specifies the target height and the
        margin, while the controller is mainly needed for its constants
        (captured in a dict) as well.
        """
        self.sensor = Sensor('127.0.0.1', 8000)
        self.pump = Pump('127.0.0.1', 8000)
        self.pump.set_state = MagicMock(return_value=True)
        self.decider = Decider(100, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

        # Dict of correct future pump actions based on the current pump
        # action and the current height (based on target height of 100)
        self.outcomes_high_or_low = {
            # (current action, height): next action
            (self.pump.PUMP_IN, 90): self.pump.PUMP_IN,
            (self.pump.PUMP_IN, 110): self.pump.PUMP_OFF,
            (self.pump.PUMP_OUT, 90): self.pump.PUMP_OFF,
            (self.pump.PUMP_OUT, 110): self.pump.PUMP_OUT,
            (self.pump.PUMP_OFF, 90): self.pump.PUMP_IN,
            (self.pump.PUMP_OFF, 110): self.pump.PUMP_OUT
        }

    def test_tick_high_or_low(self):
        """Testing tick based on decider rules 1, 2, 4, and 5."""
        for height in range(90, 111, 20):  # 90 or 110
            for action in self.controller.actions.values():  # in -> off -> out
                self.sensor.measure = MagicMock(return_value=height)
                self.pump.get_state = MagicMock(return_value=action)
                self.controller.tick()
                self.pump.set_state.assert_called_with(
                    self.outcomes_high_or_low[(action, height)])

    def test_tick_medium_and_off(self):
        """Testing tick based on decider rule 3."""
        for height in range(95, 106):
            self.sensor.measure = MagicMock(return_value=height)
            self.pump.get_state = MagicMock(return_value=self.pump.PUMP_OFF)
            self.controller.tick()
            self.pump.set_state.assert_called_with(self.pump.PUMP_OFF)
