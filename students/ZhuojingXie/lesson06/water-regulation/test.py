"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from controller import Controller
from decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Decider.decide


    def test_decide(self):
        """
        Test decider's decide method
        """
        target = Decider(100, .05)
        acts = {
            'PUMP_IN': 1,
            'PUMP_OUT': -1,
            'PUMP_OFF': 0,
        }

        self.assertEqual(target.decide(80, acts['PUMP_OFF'], acts),1)
        self.assertEqual(target.decide(80, acts['PUMP_IN'], acts),1)
        self.assertEqual(target.decide(110, acts['PUMP_OFF'], acts), -1)
        self.assertEqual(target.decide(110, acts['PUMP_OUT'], acts), -1)
        self.assertEqual(target.decide(101, acts['PUMP_OFF'], acts), 0)
        self.assertEqual(target.decide(110, acts['PUMP_IN'], acts), 0)
        self.assertEqual(target.decide(80, acts['PUMP_OUT'], acts), 0)



class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick
    def test_controller_tick(self):
        sensor = Sensor('127.0.0.1', '514')
        sensor.measure = MagicMock(return_value=105)
        pump = Pump('127.0.0.1', '8000')
        pump.get_state = MagicMock(return_value='PUMP_OFF')
        pump.set_state = MagicMock(return_value='PUMP_IN')
        decider = Decider(100, 0.05)

        controller = Controller(sensor, pump, decider)

        self.assertTrue(controller.tick())
