# pylint: disable=no-self-use,duplicate-code


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

    def test_integration_test(self):  # pylint: disable=no-self-use,duplicate-code
        """ Testing the integration of waterregulation modules.

        Note: controller should return true if call to set pump state is
        successful.  Not responsible for judging values, just returns.
        """
        pump = Pump('127.0.0.1', '8000')
        sensor = Sensor('127.0.0.1', '8000')
        decider = Decider(120, .07)
        controller = Controller(sensor, pump, decider)

        actions = {
            'PUMP_IN': 1,
            'PUMP_OUT': -1,
            'PUMP_OFF': 0
        }

        controller.pump.set_state = MagicMock(return_value=True)
        for action in controller.actions.values():
            for level in range(20, 170, 10):
                controller.sensor.measure = MagicMock(return_value=level)
                # The get_state should be determined by a mocked value using
                # the water levels vs all 3 actions in the action dict.
                controller.pump.get_state = MagicMock(
                    decider.decide(level, action, actions))
                controller.tick()
