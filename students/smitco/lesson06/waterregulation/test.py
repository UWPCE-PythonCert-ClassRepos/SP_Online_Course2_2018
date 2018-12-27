"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from controller import Controller
from decider import Decider

from pump.pump import Pump
from sensor.sensor import Sensor


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def setUp(self):
        """Set up decider for tests"""

        self.actions = {
            'PUMP_IN': 'PUMP_IN',
            'PUMP_OUT': 'PUMP_OUT',
            'PUMP_OFF': 'PUMP_OFF'
        }

        self.decider = Decider(10, 0.05)

    def test_decide_1(self):
        """The *decide* method shall obey the following behaviors:

           1. If the pump is off and the height is below the margin region,
           then the pump should be turned to PUMP_IN."""

        self.assertEqual('PUMP_IN', self.decider.decide(8, 'PUMP_OFF'))

    def test_decide_2(self):
        """The *decide* method shall obey the following behaviors:

           2. If the pump is off and the height is above the margin region,
           then the pump should be turned to PUMP_OUT."""

        self.assertEqual('PUMP_OUT', self.decider.decide(12, 'PUMP_OFF'))

    def test_decide_3(self):
        """The *decide* method shall obey the following behaviors:

            3. If the pump is off and the height is within the margin region
            or on the exact boundary of the margin region, then the pump
            shall remain at PUMP_OFF."""

        self.assertEqual('PUMP_OFF', self.decider.decide(10, 'PUMP_OFF'))
        self.assertEqual('PUMP_OFF', self.decider.decide(10.5, 'PUMP_OFF'))
        self.assertEqual('PUMP_OFF', self.decider.decide(9.5, 'PUMP_OFF'))

    def test_decide_4(self):
        """The *decide* method shall obey the following behaviors:

            4. If the pump is performing PUMP_IN and the height is above
            target height, then the pump shall be turned to PUMP_OFF,
            otherwise the pump shall remain at PUMP_IN."""

        self.assertEqual('PUMP_OFF', self.decider.decide(11, 'PUMP_IN'))
        self.assertEqual('PUMP_IN', self.decider.decide(9, 'PUMP_IN'))

    def test_decide_5(self):
        """The *decide* method shall obey the following behaviors:

            5. If the pump is performing PUMP_OUT and the height is below the
            target height, then the pump shall be turned to PUMP_OFF,
            otherwise the pump shall remain at PUMP_OUT."""

        self.assertEqual('PUMP_OFF', self.decider.decide(7, 'PUMP_OUT'))
        self.assertEqual('PUMP_OUT', self.decider.decide(13, 'PUMP_OUT'))

    def test_decide_wrong_action(self):
        """Test for error message if current action not in action dict"""

        self.assertFalse(self.decider.decide(10, "Unknown"))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        """Set up controller for test"""

        self.sensor = Sensor('127.0.0.1', 8000)
        self.pump = Pump('127.0.0.1', 8000)
        self.decider = Decider(10, 0.05)
        self.controller = Controller(self.sensor, self.pump, self.decider)

    def test_controller(self):
        """test controller tick method"""

        self.sensor.measure = MagicMock(return_value=11.3)
        self.pump.get_state = MagicMock(return_value='PUMP_IN')
        self.pump.set_state = MagicMock(return_value=True)
        self.decider.decide = MagicMock(return_value='PUMP_OFF')

        self.controller.tick()

        self.pump.set_state.assert_called_with('PUMP_OFF')
