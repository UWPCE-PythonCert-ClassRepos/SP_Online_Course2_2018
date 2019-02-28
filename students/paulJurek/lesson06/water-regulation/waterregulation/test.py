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
    def setUp(self):
        """sets up reusable Decider for rest of test"""
        self.decider = Decider(target_height=100, margin=.1)
        self.actions = {
            'PUMP_IN': 1,
            'PUMP_OUT': -1,
            'PUMP_OFF': 0,
        }

    def test_get_target_low(self):
        """assures get_target_low provides correct value"""
        self.assertEqual(90, int(self.decider.get_target_low()))

    def test_get_target_high(self):
        """assures get_target_high provides correct value"""
        self.assertEqual(110, int(self.decider.get_target_high()))

    def test_pump_in_for_off_pump_low_height(self):
        """1. If the pump is off and the height is below the
        margin region, then the pump should be turned to PUMP_IN."""
        # set current state
        current_height = (self.decider.target_height *
                          (1 - 2 * self.decider.margin))
        pump_state = 'PUMP_OFF'

        self.assertEqual(self.actions['PUMP_IN'],
                         self.decider.decide(current_height=current_height,
                                             current_action=pump_state,
                                             actions=self.actions))

    def test_pump_out_for_pump_off_height_above(self):
        """2. If the pump is off and the height is above the margin region,
        then the pump should be turned to PUMP_OUT."""
        # set current state
        current_height = (self.decider.target_height
                          * (1 + 2 * self.decider.margin))
        pump_state = 'PUMP_OFF'

        self.assertEqual(self.actions['PUMP_OUT'],
                         self.decider.decide(current_height=current_height,
                                             current_action=pump_state,
                                             actions=self.actions))

    def test_pump_off_for_pump_off_height_good(self):
        """3. If the pump is off and the height is within the margin
        region or on the exact boundary of the margin region, then
        the pump shall remain at PUMP_OFF."""
        # set current state
        current_height = self.decider.target_height
        pump_state = 'PUMP_OFF'

        self.assertEqual(self.actions['PUMP_OFF'],
                         self.decider.decide(current_height=current_height,
                                             current_action=pump_state,
                                             actions=self.actions))

    def test_pump_off_for_height_above_pump_in(self):
        """4. If the pump is performing PUMP_IN and the height is above
             the target height, then the pump shall be turned to PUMP_OFF,
             otherwise the pump shall remain at PUMP_IN.
        """
        # set current state
        current_height = (self.decider.target_height
                          * (1 + 2 * self.decider.margin))
        pump_state = 'PUMP_IN'

        self.assertEqual(self.actions['PUMP_OFF'],
                         self.decider.decide(current_height=current_height,
                                             current_action=pump_state,
                                             actions=self.actions))

    def test_pump_in_for_height_low_pump_in(self):
        """4. If the pump is performing PUMP_IN and the height is above
             the target height, then the pump shall be turned to PUMP_OFF,
             otherwise the pump shall remain at PUMP_IN.
        """
        # set current state
        current_height = self.decider.target_height
        pump_state = 'PUMP_IN'

        self.assertEqual(self.actions['PUMP_IN'],
                         self.decider.decide(current_height=current_height,
                                             current_action=pump_state,
                                             actions=self.actions))

    def test_pump_off_for_pump_out_height_low(self):
        """5. If the pump is performing PUMP_OUT and the height is below
             the target height, then the pump shall be turned to PUMP_OFF,
             otherwise, the pump shall remain at PUMP_OUT.
        """
        # set current state
        current_height = (self.decider.target_height
                          * (1 - 2 * self.decider.margin))
        pump_state = 'PUMP_OUT'

        self.assertEqual(self.actions['PUMP_OFF'],
                         self.decider.decide(current_height=current_height,
                                             current_action=pump_state,
                                             actions=self.actions))

    def test_pump_out_for_pump_out_height_hight(self):
        """5. If the pump is performing PUMP_OUT and the height is below
             the target height, then the pump shall be turned to PUMP_OFF,
             otherwise, the pump shall remain at PUMP_OUT.
        """
        # set current state
        current_height = self.decider.target_height
        pump_state = 'PUMP_OUT'

        self.assertEqual(self.actions['PUMP_OUT'],
                         self.decider.decide(current_height=current_height,
                                             current_action=pump_state,
                                             actions=self.actions))


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    def setUp(self):
        self.sensor = Sensor('127.0.0.1', 8000)
        self.pump = Pump('127.0.0.1', 8000)
        self.decider = Decider('127.0.0.1', 8000)

        self.controller = Controller(sensor=self.sensor,
                                     pump=self.pump,
                                     decider=self.decider)

    def test_measure_is_called(self):
        """given controller with sensor attached
        when get_measurement is called, the sensor measure method
        gets called"""
        self.sensor.measure = MagicMock(return_value=0)

        self.controller.get_measurement()
        self.sensor.measure.assert_called_with()

    def test_get_pump_state_called(self):
        """given controoler with pump
        when controller get_pump_state called
        the pump method get_state gets called"""
        self.pump.get_state = MagicMock(return_value=0)

        self.controller.get_pump_state()
        self.pump.get_state.assert_called_with()

    def test_decider_gets_called(self):
        """given a controller
        when decide_pump_state gets called
        decider method decide gets called with inputs
        for current fluid height and pump state"""
        self.decider.decide = MagicMock(return_value='PUMP_OFF')

        self.controller.decide_pump_state(current_height=5.0,
                                          pump_state='PUMP_OFF',
                                          actions=self.controller.actions)
        self.decider.decide.assert_called_with(current_height=5.0,
                                               current_action='PUMP_OFF',
                                               actions=self.controller.actions)

    def test_tick_runs_process_to_set_pump_state(self):
        """
        expected behavior
        1. query the sensor for the current height of liquid in the tank
          2. query the pump for its current state (pumping in,
            pumping out, or at rest)
          3. query the decider for the next appropriate state of the pump,
            given the above
          4. set the pump to that new state
        """
        current_height = 5
        pump_state = 'PUMP_OFF'
        next_pump_state = 'PUMP_IN'

        self.sensor.measure = MagicMock(return_value=current_height)
        self.pump.get_state = MagicMock(return_value=pump_state)
        decider_return = self.controller.actions[next_pump_state]
        self.decider.decide = MagicMock(return_value=decider_return)
        self.pump.set_state = MagicMock(return_value=True)

        self.controller.tick()

        self.sensor.measure.assert_called_with()
        self.pump.get_state.assert_called_with()
        self.decider.decide.assert_called_with(current_height=current_height,
                                               current_action=pump_state,
                                               actions=self.controller.actions)
