"""
Module tests for the water-regulation module
"""

import unittest
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from .controller import Controller
from .decider import Decider


class ModuleTests(unittest.TestCase):
    """
    Module tests for the water-regulation module
    """

    def test_integration(self):
        """Integration test combining controller and decider."""

        di = Decider(100, 0.05)
        pi = Pump('127.0.0.1', '8000')
        si = Sensor('127.0.0.2', '8000')
        ci = Controller(si, pi, di)

