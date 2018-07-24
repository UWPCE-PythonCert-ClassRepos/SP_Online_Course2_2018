"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from waterregulation.pump import Pump
from waterregulation.sensor import Sensor

from waterregulation.controller import Controller
from waterregulation.decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def setUp(self):

        self.pump = Pump('127.0.0.1', '8000')
        self.sensor = Sensor('127.0.0.1', '8001')
        self.decider = Decider(100, 2)
        self.controller = Controller(self.sensor, self.pump, self.decider)
        self.controller.pump.set_state = MagicMock(return_value=True)

    def test_water_regulation(self):
        """ test all actions and range of water levels around target height """

        for action in self.controller.actions.values():
            for water_level in range(90, 110, 2):
                
                # measure water level
                self.controller.sensor.measure = MagicMock(return_value = water_level)

                # get the state of the pump
                self.controller.pump.get_state = MagicMock(return_value = self.decider.decide(water_level, action, self.controller.actions))

                self.controller.tick()

        self.assertTrue(True)

if __name__ == '__main__':

    unittest.main()
