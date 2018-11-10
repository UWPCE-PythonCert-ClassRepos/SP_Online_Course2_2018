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

    def test_decide(self):
        """
        Tests for the decide method

          Test steps performed below:

          1. If the pump is off and the height is below the margin region, then
             the pump should be turned to PUMP_IN.
          2. If the pump is off and the height is above the margin region, then
             the pump should be turned to PUMP_OUT.
          3. If the pump is off and the height is within the margin region or
             on the exact boundary of the margin region, then the pump shall
             remain at PUMP_OFF.
          4. If the pump is performing PUMP_IN and the height is above the
             target height, then the pump shall be turned to PUMP_OFF,
             otherwise the pump shall remain at PUMP_IN.
          5. If the pump is performing PUMP_OUT and the height is below the
             target height, then the pump shall be turned to PUMP_OFF,
             otherwise, the pump shall remain at PUMP_OUT.
        """

        sensor = Sensor("127.0.0.1", "5150")
        pump = Pump("127.0.0.1", "5051")
        decider = Decider(500, .05)

        controller = Controller(sensor, pump, decider)
        actions = controller.actions

        self.assertEqual(decider.decide(400.0, Pump.PUMP_OFF, actions),
                         Pump.PUMP_IN)
        self.assertEqual(decider.decide(530.0, Pump.PUMP_OFF, actions),
                         Pump.PUMP_OUT)
        self.assertEqual(decider.decide(500.0, Pump.PUMP_OFF, actions),
                         Pump.PUMP_OFF)

        self.assertEqual(decider.decide(530.0, Pump.PUMP_IN, actions),
                         Pump.PUMP_OFF)
        self.assertEqual(decider.decide(400.0, Pump.PUMP_IN, actions),
                         Pump.PUMP_IN)

        self.assertEqual(decider.decide(530.0, Pump.PUMP_OUT, actions),
                         Pump.PUMP_OUT)
        self.assertEqual(decider.decide(400.0, Pump.PUMP_OUT, actions),
                         Pump.PUMP_OFF)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick(self):
        """
        Tests for the tick method
        """
        sensor = Sensor("127.0.0.1", "5150")
        pump = Pump("127.0.0.1", "5051")
        decider = Decider(500, .05)

        controller = Controller(sensor, pump, decider)
        actions = controller.actions

        sensor.measure = MagicMock(return_value=400.0)
        pump.get_state = MagicMock(return_value=Pump.PUMP_OFF)
        decider.decide = MagicMock(return_value=Pump.PUMP_IN)
        pump.set_state = MagicMock(return_value=True)

        controller.tick()

        decider.decide.assert_called_with(sensor.measure(), pump.get_state(),
                                          actions)
