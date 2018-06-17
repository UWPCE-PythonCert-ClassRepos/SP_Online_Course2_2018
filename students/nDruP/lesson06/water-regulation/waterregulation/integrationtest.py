"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from controller import Controller
from decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def test_module(self):
        """
        Go through various sensor.measure and pump.get_state values to verify
        the compatibility of decider and controller.
        """
        dec = Decider(100, .05)
        control = Controller(
            Sensor("127.0.0.1", "8000"),
            Pump("127.0.0.1", "8000"),
            dec
        )

        control.pump.set_state = MagicMock(return_value=True)

        levels = [110, 90, 99]

        for pump_act in control.actions.values():
            control.pump.get_state = MagicMock(return_value=pump_act)
            for water_h in levels:
                control.sensor.measure = MagicMock(return_value=water_h)
                control.tick()
                control.pump.get_state = MagicMock(
                    return_value=dec.decide(
                        control.sensor.measure(),
                        control.pump.get_state(),
                        control.actions
                    )
                )
