"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider

pump = Pump('127.0.0.1', 8000)
sensor = Sensor('127.0.0.1', 8000)

actions = {
    'PUMP_IN': pump.PUMP_IN,
    'PUMP_OUT': pump.PUMP_OUT,
    'PUMP_OFF': pump.PUMP_OFF,
}


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def test_decider(self):
        """A function to test various inputs and outputs of
        decider module"""

        decider = Decider(50, .05)

        test1 = decider.decide(30, actions['PUMP_OFF'], actions)
        self.assertEqual(actions['PUMP_IN'], test1)

        test2 = decider.decide(70, actions['PUMP_OFF'], actions)
        self.assertEqual(actions['PUMP_OUT'], test2)

        test3 = decider.decide(50, actions['PUMP_OFF'], actions)
        self.assertEqual(actions['PUMP_OFF'], test3)

        test4 = decider.decide(55, actions['PUMP_IN'], actions)
        self.assertEqual(actions['PUMP_OFF'], test4)

        test5 = decider.decide(45, actions['PUMP_IN'], actions)
        self.assertEqual(actions['PUMP_IN'], test5)

        test6 = decider.decide(45, actions['PUMP_OUT'], actions)
        self.assertEqual(actions['PUMP_OFF'], test6)

        test7 = decider.decide(55, actions['PUMP_OUT'], actions)
        self.assertEqual(actions['PUMP_OUT'], test7)


class ControllerTests(unittest.TestCase):
    """Unit tests for the Controller class"""

    def test_controller_tick(self):
        """Function to test a tick of controller module"""
        decider = Decider(50, .05)
        controller = Controller(sensor, pump, decider)

        sensor.measure = MagicMock(return_value=25)
        pump.get_state = MagicMock(return_value=pump.PUMP_OFF)
        decider.decide = MagicMock(return_value=pump.PUMP_IN)
        pump.set_state = MagicMock(return_value=True)

        controller.tick()

        decider.decide.assert_called_with(25, pump.PUMP_OFF, actions)
        sensor.measure.assert_called_with()
        pump.get_state.assert_called_with()
