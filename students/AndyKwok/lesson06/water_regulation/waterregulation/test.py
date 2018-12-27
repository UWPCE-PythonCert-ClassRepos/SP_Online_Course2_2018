"""
Unit tests for the water-regulation module
"""
import unittest
from unittest.mock import MagicMock
from pump.pump import Pump
from sensor.sensor import Sensor
from .controller import Controller
from .decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def test_decide(self):
        """
        Testing Decider.decide
        """
        actions = {'PUMP_IN': 1,
                   'PUMP_OUT': -1,
                   'PUMP_OFF': 0}
        test_unit = Decider(10, 0.1)
        self.assertEqual('PUMP_IN', test_unit.decide(9, 'PUMP_OFF', actions))
        self.assertEqual('PUMP_OUT', test_unit.decide(11, 'PUMP_OFF', actions))
        self.assertEqual('PUMP_OFF', test_unit.decide(10, 'PUMP_OFF', actions))
        self.assertEqual('PUMP_OFF', test_unit.decide(11, 'PUMP_IN', actions))
        self.assertEqual('PUMP_IN', test_unit.decide(9, 'PUMP_IN', actions))
        self.assertEqual('PUMP_OFF', test_unit.decide(9, 'PUMP_OUT', actions))
        self.assertEqual('PUMP_OUT', test_unit.decide(11, 'PUMP_OUT', actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick(self):
        """
        Testing Sensor.tick
        """
        sensor = Sensor('127.0.0.1', '8000')
        sensor.measure = MagicMock(return_value=10)
        pump = Pump('127.0.0.1', '8000')
        pump.get_state = MagicMock(return_value='PUMP_OFF')
        pump.set_state = MagicMock(return_value='PUMP_OFF')
        decider = Decider(10, 0.1)
        decider.decide = MagicMock(return_value='PUMP_OFF')
        controller = Controller(sensor, pump, decider)
        self.assertTrue(controller.tick())


class DummyTests(unittest.TestCase):
    """
    Dummy Test
    """

    def test_dummy(self):
        """
        Force pass flake8 & pylint
        """
        dummy = Decider(10, 0.1)
        dummy_margin = dummy.dummy()
        self.assertEqual(0.1, dummy_margin)
