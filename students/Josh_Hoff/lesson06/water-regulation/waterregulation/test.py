"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """
    def test_decider(self):
    
        actions = {'PUMP_IN': -1, 'PUMP_OUT': 0, 'PUMP_OFF': 1}
        
        decider = Decider(80, .05)
        
        decider.decide(70, 0, actions)
    # TODO: write a test or tests for each of the behaviors defined for
    #       Decider.decide

#    def test_dummy(self):
#        """
#        Just some example syntax that you might use
#        """
#
#        pump = Pump('127.0.0.1', 8000)
#        pump.set_state = MagicMock(return_value=True)
#
#        self.fail("Remove this test.")


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """
    def test_controller(self):
    
        pump = Pump('0.0.0.1', 541)
        # TODO: write a test or tests for each of the behaviors defined for
        #       Controller.tick

#        pass
