#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import MagicMock
import time

from great_circle_v0 import great_circle as gc0
from great_circle_v1 import great_circle as gc1
from great_circle_v2 import great_circle as gc2


class great_circle_tests(TestCase):

    def setUp(self):
        self.lon1, self.lat1, self.lon2, self.lat2 = -72.345, 34.323, -61.823, 54.826

    def test_gc0(self):

        gc = gc0(self.lon1, self.lat1, self.lon2, self.lat2)

        self.assertEqual(round(gc, 3), 1503.393)

    def test_gc1(self):
        # lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 54.826
        gc = gc1(self.lon1, self.lat1, self.lon2, self.lat2)

        self.assertEqual(round(gc, 3), 1503.393)

    def test_gc2(self):
        # lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 54.826
        gc = gc2(self.lon1, self.lat1, self.lon2, self.lat2)

        self.assertEqual(round(gc, 3), 1503.393)

    def test_time_diffs(self):
        start_time_0 = time.time()

        for i in range(10000000):
            gc0(self.lon1, self.lat1, self.lon2, self.lat2)
        end_time_0 = (time.time() - start_time_0)

        start_time_1 = time.time()

        for i in range(10000000):
            gc1(self.lon1, self.lat1, self.lon2, self.lat2)
        end_time_1 = (time.time() - start_time_1)

        start_time_2 = time.time()

        for i in range(10000000):
            gc2(self.lon1, self.lat1, self.lon2, self.lat2)
        end_time_2 = (time.time() - start_time_2)

        self.assertGreater(end_time_0, end_time_1)
        self.assertGreater(end_time_1, end_time_2)
