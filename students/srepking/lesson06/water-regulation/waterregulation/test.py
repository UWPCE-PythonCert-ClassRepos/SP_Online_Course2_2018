"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from waterregulation.pump.pump import Pump
from waterregulation.sensor.sensor import Sensor
from waterregulation.controller import Controller
from waterregulation.decider import Decider


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def setUp(self):
        """Setup DeciderTests"""
        self.sensor = Sensor('127.0.0.1', 8001)
        self.pump = Pump('127.0.0.1', 8000)
        self.decider = Decider(5, .05)
        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

    def test_pump_off_height_low(self):
        """1. If the pump is off and the height is below the margin region,
        then the
             pump should be turned to PUMP_IN."""
        self.sensor.measure = MagicMock(return_value=4)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=0)
        pump_status = self.pump.get_state()
        self.assertEqual(1, self.decider.decide(measurement, pump_status,
                                                self.actions))

    def test_pump_off_height_high(self):
        """2. If the pump is off and the height is above the margin region,
        then the
             pump should be turned to PUMP_OUT."""
        self.sensor.measure = MagicMock(return_value=6)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=0)
        pump_status = self.pump.get_state()
        self.assertEqual(-1, self.decider.decide(measurement, pump_status,
                                                 self.actions))

    def test_pump_off_height_plus_margin(self):
        """3. If the pump is off and the height is within the margin region
        or on
             the exact boundary of the margin region, then the pump shall
             remain at
             PUMP_OFF.
          """
        self.sensor.measure = MagicMock(return_value=5.05)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=0)
        pump_status = self.pump.get_state()
        self.assertEqual(0, self.decider.decide(measurement, pump_status,
                                                self.actions))

    def test_pump_off_height_minus_margin(self):
        """3. If the pump is off and the height is within the margin
        region or on
             the exact boundary of the margin region, then the pump
             shall remain at
             PUMP_OFF.
          """
        self.sensor.measure = MagicMock(return_value=4.95)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=0)
        pump_status = self.pump.get_state()
        self.assertEqual(0, self.decider.decide(measurement, pump_status,
                                                self.actions))

    def test_pump_in_height_high(self):
        """4. If the pump is performing PUMP_IN and the height is above
        the target
             height, then the pump shall be turned to PUMP_OFF, otherwise
             the pump
             shall remain at PUMP_IN.
          """
        self.sensor.measure = MagicMock(return_value=5.01)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=1)  # PUMP_IN
        pump_status = self.pump.get_state()
        self.assertEqual(0, self.decider.decide(measurement, pump_status,
                                                self.actions))

    def test_pump_in_height_low(self):
        """4. If the pump is performing PUMP_IN and the height is above
        the target
             height, then the pump shall be turned to PUMP_OFF, otherwise
             the pump
             shall remain at PUMP_IN.
          """
        self.sensor.measure = MagicMock(return_value=4.99)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=1)  # PUMP_IN
        pump_status = self.pump.get_state()
        self.assertEqual(1, self.decider.decide(measurement, pump_status,
                                                self.actions))

    def test_pump_out_height_low(self):
        """5. If the pump is performing PUMP_OUT and the height is below
        the target
             height (5), then the pump shall be turned to PUMP_OFF."""
        self.sensor.measure = MagicMock(return_value=4.99)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=-1)  # PUMP_OUT
        pump_status = self.pump.get_state()
        self.assertEqual(0, self.decider.decide(measurement, pump_status,
                                                self.actions))

    def test_pump_out_height_high(self):
        """5. If the pump is performing PUMP_OUT and the height is
        greater than or equal to the target
             height (5), then the pump shall remain at PUMP_OUT."""
        self.sensor.measure = MagicMock(return_value=5.0)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=-1)  # PUMP_OUT
        pump_status = self.pump.get_state()
        self.assertEqual(-1, self.decider.decide(measurement, pump_status,
                                                 self.actions))

    def test_bad_pump_status(self):
        """Raise Exception for Bad Pump Status"""
        self.sensor.measure = MagicMock(return_value=5.0)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=-2)  # Enter Bad Pump
        # Status
        pump_status = self.pump.get_state()
        with self.assertRaises(Exception):
            self.decider.decide(measurement, pump_status, self.actions)

    def test_bad_height_setting(self):
        """Raise Exception for Bad Height Setting"""

        with self.assertRaises(Exception):
            self.decider = Decider(-1, .05)

    def test_bad_sensor_status(self):
        """Raise Exception for Bad Sensor Reading. Levels can't be negative."""
        self.sensor.measure = MagicMock(return_value=-2)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=0)  # Enter Bad Sensor
        # Status
        pump_status = self.pump.get_state()
        with self.assertRaises(Exception):
            self.decider.decide(measurement, pump_status, self.actions)


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """
    def setUp(self):
        self.sensor = Sensor('127.0.0.1', '8001')
        self.pump = Pump('127.0.0.1', '8000')
        self.decider = Decider(5, .05)
        self.new_controller = Controller(self.sensor, self.pump, self.decider)
        self.actions = {
            'PUMP_IN': self.pump.PUMP_IN,
            'PUMP_OUT': self.pump.PUMP_OUT,
            'PUMP_OFF': self.pump.PUMP_OFF,
        }

    def test_current_height(self):
        """1. query the sensor for the current height of liquid in the tank"""

        self.sensor.measure = MagicMock(return_value=2)
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=0)  # PUMP_OFF
        self.pump.set_state = MagicMock(return_value=True)
        self.new_controller.tick()  # update values of tick
        self.assertEqual(self.new_controller.liquid_level, measurement)

    def test_pump_status(self):
        """query the pump for its current state (pumping in, pumping out,
        or at rest)"""

        self.sensor.measure = MagicMock(return_value=2)
        self.pump.get_state = MagicMock(return_value=0)  # PUMP_OFF
        pump_status = self.pump.get_state()
        self.pump.set_state = MagicMock(return_value=True)
        self.new_controller.tick()  # update values of tick
        self.assertEqual(self.new_controller.pump_status, pump_status)

    def test_query_decider(self):

        """query the decider for the next appropriate state of the pump,
        given the above"""
        self.sensor.measure = MagicMock(return_value=2)  # Set Liquid Level
        # to 2
        measurement = self.sensor.measure()
        self.pump.get_state = MagicMock(return_value=0)  # PUMP_OFF
        pump_state = self.pump.get_state()
        self.pump.set_state = MagicMock(return_value=True)
        self.new_controller.tick()  # update values of tick
        # with pump off and liquid level to 2, the pump should be turned on.
        decision = self.decider.decide(measurement, pump_state, self.actions)
        self.assertEqual(self.new_controller.control_decision, decision)

    def test_set_pump_ok(self):
        """set the pump to that new state. With pump off and
        liquid level to 2, the pump should be turned on"""

        self.sensor.measure = MagicMock(return_value=2)  # Set Liquid Level
        # to 2
        self.pump.get_state = MagicMock(return_value=0)  # PUMP_OFF
        self.pump.set_state = MagicMock(return_value=True)  # Assume pump
        # set OK
        self.new_controller.tick()  # update values of tick
        self.assertTrue(self.new_controller.tick() is True)

    def test_set_pump_not_ok(self):
        """set the pump to that new state. With pump off and
        liquid level to 2, the pump should be turned on"""

        self.sensor.measure = MagicMock(return_value=2)  # Set Liquid Level
        # to 2
        self.pump.get_state = MagicMock(return_value=0)  # PUMP_OFF
        self.pump.set_state = MagicMock(return_value=False)  # Assume pump
        # set Not OK
        self.new_controller.tick()  # update values of tick
        self.assertTrue(self.new_controller.tick() is False)
