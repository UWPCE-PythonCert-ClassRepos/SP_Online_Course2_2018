"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    #       using a MOCKED sensor and pump.

    def test_module(self):

        target = Decider(100, .05)
        controller = Controller(Sensor("127.0.0.1", 8080),
                                Pump("127.0.0.1", 8050), target)
        controller.pump.set_state = MagicMock(return_value=True)

        for action in controller.actions.values():
            controller.pump.get_state = MagicMock(return_value=action)
            for levels in range(90, 115, 5):
                controller.sensor.measure = MagicMock(return_value=levels)
                controller.tick()
                controller.pump.get_state = MagicMock(
                    return_value=target.decide(
                        controller.sensor.measure(),
                        controller.pump.get_state(),
                        controller.actions
                    ))
