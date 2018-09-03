"""
Unit tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock
import urllib.request

from pump import Pump
from sensor import Sensor

from .decider import Decider
from .controller import Controller  # noqa pylint: disable=unused-import
from .integrationtest import do_tick


class DeciderTests(unittest.TestCase):
    """
    Unit tests for the Decider class
    """

    def test_decider(self):
        """Make next determination."""
        actions = {
            'PUMP_IN': 1,
            'PUMP_OFF': 0,
            'PUMP_OUT': -1,
        }
        decider = Decider(10, 0.05)

        # Case 1: Pump: OFF, height < margin --> IN
        result = decider.decide(5, actions['PUMP_OFF'], actions)
        self.assertEqual(result, actions['PUMP_IN'])

        # Case 2: Pump: OFF, height > margin --> OUT
        result = decider.decide(15, actions['PUMP_OFF'], actions)
        self.assertEqual(result, actions['PUMP_OUT'])

        # Case 3: Pump: OFF, height > margin --> OFF
        idx = 9.5
        while idx <= 10.5:
            result = decider.decide(idx, actions['PUMP_OFF'], actions)
            self.assertEqual(result, actions['PUMP_OFF'])
            idx += 0.1

        # Case 4a: Pump: IN, height > margin --> OFF
        result = decider.decide(15, actions['PUMP_IN'], actions)
        self.assertEqual(result, actions['PUMP_OFF'])

        # Case 4b: Pump: IN, height <= margin --> IN
        idx = 10.5
        while idx >= 5:
            result = decider.decide(idx, actions['PUMP_IN'], actions)
            self.assertEqual(result, actions['PUMP_IN'])
            idx -= 0.1

        # Case 5a: Pump: OUT, height < margin --> OFF
        result = decider.decide(5, actions['PUMP_OUT'], actions)
        self.assertEqual(result, actions['PUMP_OFF'])

        # Case 5b: Pump: OUT, height >= margin --> OUT
        idx = 9.5
        while idx <= 15:
            result = decider.decide(idx, actions['PUMP_OUT'], actions)
            self.assertEqual(result, actions['PUMP_OUT'])
            idx += 0.1


class Response(object):
    """
    Helper class.
    """
    def __init__(self, read):
        self.read = read


class ControllerTests(unittest.TestCase):
    """
    Unit tests for the Controller class
    """

    DUMMY_ADDR = '127.0.0.1'
    DUMMY_PORT = '8000'

    def test_sensor(self):
        """Test Sensor Measure."""
        urllib.request.urlopen = MagicMock(return_value=Response(5))
        sensor = Sensor(ControllerTests.DUMMY_ADDR, ControllerTests.DUMMY_PORT)
        current_height = sensor.measure()
        self.assertEqual(current_height, 5)

    def test_pump_get_state(self):
        """Test Pump Get State."""
        urllib.request.urlopen = MagicMock(return_value=Response(5))
        pump = Pump(ControllerTests.DUMMY_ADDR, ControllerTests.DUMMY_PORT)
        current_height = pump.get_state()
        self.assertEqual(current_height, 5)

    def test_pump_set_state_true(self):
        """Test Pump Set State True."""
        urllib.request.urlopen = MagicMock(return_value=Response(5))
        pump = Pump(ControllerTests.DUMMY_ADDR, ControllerTests.DUMMY_PORT)
        return_value = pump.set_state(12)
        self.assertEqual(return_value, True)

    def test_pump_set_state_false(self):
        """Test Pumpt Set State False."""
        def bad_urlopen(request):
            """Dummy function to raise an HTTPError."""
            del request  # Unused
            raise urllib.error.HTTPError(code=3, msg='A message',
                                         hdrs='some headers',
                                         fp=None, url='www.google.com')
        urllib.request.urlopen = bad_urlopen
        pump = Pump(ControllerTests.DUMMY_ADDR, ControllerTests.DUMMY_PORT)
        return_value = pump.set_state(12)
        self.assertEqual(return_value, False)

    def test_tick(self):
        """Test logic of sensor, pump."""
        do_tick()
