"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider

actions = {
    'PUMP_IN': 1,
    'PUMP_OUT': 0,
    'PUMP_OFF': -1,
}

class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    """     def test_dummy(self):
        
        Just some example syntax that you might use
        

        pump = Pump('127.0.0.1', 8000)
        pump.set_state = MagicMock(return_value=True)

        self.fail("Remove this test.") """
    
    def test_decider_off_below(self):
        decider = Decider(50,5)
        action_state = decider.decide(40,actions['PUMP_OFF'],actions)
        self.assertEqual(actions['PUMP_IN'],action_state)
    
    def test_decider_off_above(self):
        decider = Decider(50,5)
        action_state = decider.decide(60,actions['PUMP_OFF'],actions)
        self.assertEqual(actions['PUMP_OUT'],action_state)

    def test_decider_off_within(self):
        decider = Decider(50,5)
        action_state = decider.decide(51,actions['PUMP_OFF'],actions)
        self.assertEqual(actions['PUMP_OFF'],action_state)
    
    def test_decider_in_below(self):
        decider = Decider(50,5)
        action_state = decider.decide(40,actions['PUMP_IN'],actions)
        self.assertEqual(actions['PUMP_IN'],action_state)
    
    def test_decider_in_above(self):
        decider = Decider(50,5)
        action_state = decider.decide(60,actions['PUMP_IN'],actions)
        self.assertEqual(actions['PUMP_OFF'],action_state)

    def test_decider_in_within(self):
        decider = Decider(50,5)
        action_state = decider.decide(51,actions['PUMP_IN'],actions)
        self.assertEqual(actions['PUMP_IN'],action_state)

    def test_decider_out_below(self):
        decider = Decider(50,5)
        action_state = decider.decide(40,actions['PUMP_OUT'],actions)
        self.assertEqual(actions['PUMP_OFF'],action_state)
    
    def test_decider_out_above(self):
        decider = Decider(50,5)
        action_state = decider.decide(60,actions['PUMP_OUT'],actions)
        self.assertEqual(actions['PUMP_OUT'],action_state)

    def test_decider_out_within(self):
        decider = Decider(50,5)
        action_state = decider.decide(51,actions['PUMP_OUT'],actions)
        self.assertEqual(actions['PUMP_OUT'],action_state)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    # TODO: write a test or tests for each of the behaviors defined for
    #       Controller.tick
    def test_tick(self):
        # Initialize controller, decider, pump, sensor.
        sensor = Sensor('127.0.0.1', 8000)
        pump = Pump('127.0.0.1', 8000)
        decider = Decider(50,5)
        controller = Controller(sensor, pump, decider)
        
        pump.set_state = MagicMock(return_value=True)
        pump.get_state = MagicMock(return_value=pump.PUMP_OFF)
        sensor.measure = MagicMock(return_value=25)

        
        self.assertEqual(Pump.PUMP_IN,controller.tick())

