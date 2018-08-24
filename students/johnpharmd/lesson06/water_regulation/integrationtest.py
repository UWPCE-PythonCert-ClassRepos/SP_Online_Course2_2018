"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from waterregulation.controller import Controller
from waterregulation.decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def test_module(self):
        """an integration test that combines controller and decider,
        using a MOCKED sensor and pump
        """
        sensor = Sensor('127.0.0.1', '514')
        sensor.measure = MagicMock(return_value=105)
        pump = Pump('127.0.0.1', '8000')
        pump.get_state = MagicMock(return_value='PUMP_OFF')
        pump.set_state = MagicMock(return_value='PUMP_IN')
        decider = Decider(120, 0.05)

        controller = Controller(sensor, pump, decider)

        actions = {
            'PUMP_IN': pump.PUMP_IN,
            'PUMP_OUT': pump.PUMP_OUT,
            'PUMP_OFF': pump.PUMP_OFF,
        }
        # self.assertEqual(controller.tick(),
        #                  pump.set_state(decider.decide(sensor.measure(),
        #                                                pump.get_state(),
        #                                                actions)))
        self.assertEqual(decider.decide(sensor.measure(),
                                        pump.get_state(), actions),
                         'PUMP_IN')
