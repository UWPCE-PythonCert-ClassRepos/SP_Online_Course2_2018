"""
Unit tests for the water-regulation module
"""

from unittest import TestCase
from unittest.mock import MagicMock

from pump import Pump
from sensor import Sensor

from controller import Controller
from decider import Decider

actions = {
    'PUMP_IN': 1,
    'PUMP_OFF': 0,
    'PUMP_OUT': -1
}

class DeciderTests(TestCase):
    """
    Unit tests for the Decider class
    """

    def test_decider_decide(self):
        """
        Unit test for decider
        :return:
        """
        deciders = Decider(100, .10)
        decision1 = deciders.decide(85, actions['PUMP_OFF'], actions)
        decision2 = deciders.decide(115, actions['PUMP_OFF'], actions)
        decision3 = deciders.decide(105, actions['PUMP_OFF'], actions)
        decision4 = deciders.decide(105, actions['PUMP_IN'], actions)
        decision5 = deciders.decide(95, actions['PUMP_IN'], actions)
        decision6 = deciders.decide(95, actions['PUMP_OUT'], actions)
        decision7 = deciders.decide(105, actions['PUMP_OUT'], actions)
        self.assertEqual(actions['PUMP_IN'], decision1)
        self.assertEqual(actions['PUMP_OUT'], decision2)
        self.assertEqual(actions['PUMP_OFF'], decision3)
        self.assertEqual(actions['PUMP_OFF'], decision4)
        self.assertEqual(actions['PUMP_IN'], decision5)
        self.assertEqual(actions['PUMP_OFF'], decision6)
        self.assertEqual(actions['PUMP_OUT'], decision7)


class ControllerTests(TestCase):
    """
    Unit tests for the Controller class
    """

    def test_tick(self):
        p = Pump('127.0.0.1', 8080)
        s = Sensor('127.0.0.1', 8083)
        d = Decider(100, .10)
        c = Controller(s, p, d)
        s.measure = MagicMock(return_value=95)
        p.get_state = MagicMock(return_value=p.PUMP_IN)
        d.decide = MagicMock(return_value=p.PUMP_IN)
        p.set_state = MagicMock(return_value=True)
        c.tick()
        s.measure.assert_called_with()
        p.get_state.assert_called_with()
        d.decide.assert_called_with(95, p.PUMP_IN, actions)
