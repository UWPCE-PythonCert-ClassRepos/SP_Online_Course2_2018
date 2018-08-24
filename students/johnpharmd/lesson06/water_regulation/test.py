"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from waterregulation.controller import Controller
from waterregulation.decider import Decider


class SensorTests(unittest.TestCase):
    """Unit tests for the Sensor class"""

    def test_sensor_call(self):
        """Tests whether fictional sensor replies to MagicMock call"""
        sensor = Sensor('127.0.0.1', 514)
        sensor.measure = MagicMock(return_value=105)

        self.assertTrue(sensor.measure())


class PumpTests(unittest.TestCase):
    """Unit tests for the Pump class"""

    def setUp(self):
        self.pump = Pump('127.0.0.1', 8000)

    def test_pump_get_state(self):
        """Tests whether pump state can be obtained"""
        self.pump.get_state = MagicMock(return_value='PUMP_OFF')

    def test_pump_set_state(self):
        """Tests whether pump state can be set"""
        self.pump.set_state = MagicMock(return_value='PUMP_OFF')
        self.assertTrue(self.pump.set_state('PUMP_OFF'))


class DeciderTests(unittest.TestCase):
    """Unit tests for the Decider class"""

    def setUp(self):
        self.decider_dict = {'PUMP_OFF': 'maintain current level',
                             'PUMP_IN': 'pump water in',
                             'PUMP_OUT': 'pump water out'}
        self.decider = Decider(120, 0.05)

    def test_lowLevel_pumpOff(self):
        """Tests if decider 'chooses' to pump in, given low level
        and pump currently off
        """
        self.assertEqual(self.decider.decide(105, 'PUMP_OFF',
                         self.decider_dict), 'pump water in')

    def test_hiLevel_pumpOff(self):
        """Tests if decider 'chooses' to pump out, given high
        level and pump currently off
        """
        self.assertEqual(self.decider.decide(140, 'PUMP_OFF',
                         self.decider_dict), 'pump water out')

    def test_okLevel_pumpOff(self):
        """Tests if decider 'chooses' to keep pump off, given level
        within margin and pump currently off
        """
        self.assertEqual(self.decider.decide(125, 'PUMP_OFF',
                         self.decider_dict), 'maintain current level')

    def test_hiLevel_pumpIn(self):
        """Tests if decider 'chooses' to turn pump off, given high
        level and pump currently in
        """
        self.assertEqual(self.decider.decide(130, 'PUMP_IN',
                         self.decider_dict), 'maintain current level')

    def test_lowLevel_pumpOut(self):
        """Tests if decider 'chooses' to turn pump off, given low
        level and pump currently out
        """
        self.assertEqual(self.decider.decide(110, 'PUMP_OUT',
                         self.decider_dict), 'maintain current level')


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick

    def setUp(self):
        self.sensor = Sensor('127.0.0.1', 514)
        self.pump = Pump('127.0.0.1', 8000)
        self.decider = Decider(120, 0.05)

        self.controller = Controller(self.sensor, self.pump, self.decider)
