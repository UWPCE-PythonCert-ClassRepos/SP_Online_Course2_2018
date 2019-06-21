"""
Module tests for the water-regulation module
"""
import sys
sys.path.insert(0, '../pump')
sys.path.insert(0, '../sensor')


import unittest
from unittest.mock import MagicMock


from pump import Pump
from sensor import Sensor


from controller import Controller
from decider import Decider

class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """


    def test_water(self):
        """
        Integration test
        """
        pump_address = Pump('127.0.0.1', '8000')
        
        
        sensor_address = Sensor('127.0.0.1', '8000')
        decider_vals = Decider(1000.0, .10)
        controller_all = Controller(sensor_address, pump_address, decider_vals)
        controller_all.pump.set_state = MagicMock(return_value=True)
        for action in controller_all.actions.values():
            for water_level in range(500, 2000, 50):
                controller_all.sensor.measure = MagicMock(return_value=water_level)
                controller_all.pump.get_state = MagicMock(return_value=decider_vals.decide(water_level,action,controller_all.actions))                
                self.assertTrue(controller_all.tick())
