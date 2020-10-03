import unittest

from datetime import date
from unittest.mock import Mock

import source.date_utils as date_utils


def format_date(date):
    return date.strftime("%B %-d")


class TestDateUtils(unittest.TestCase):
    def setUp(self):
        date_utils.actually_today = Mock()
        date_utils.get_day_offset = Mock()

        date_utils.get_day_offset.return_value = 0

    def tearDown(self):
        date_utils.actually_today.reset_mock()

    def test_today(self):
        date_utils.actually_today.return_value = date(2020, 1, 2)

        self.assertEqual(format_date(date_utils.today()), "January 2")

    def test_today_with_day_offset(self):
        date_utils.actually_today.return_value = date(2020, 1, 2)
        date_utils.get_day_offset.return_value = 1

        self.assertEqual(format_date(date_utils.today()), "January 1")

    def test_is_monday(self):
        # January 6, 2020 is a Monday
        date_utils.actually_today.return_value = date(2020, 1, 6)

        self.assertTrue(date_utils.is_monday())

        date_utils.actually_today.return_value = date(2020, 1, 7)

        self.assertFalse(date_utils.is_monday())

    def test_is_monday_with_day_offset(self):
        date_utils.actually_today.return_value = date(2020, 1, 6)
        date_utils.get_day_offset.return_value = 1

        self.assertFalse(date_utils.is_monday())

        date_utils.actually_today.return_value = date(2020, 1, 7)

        self.assertTrue(date_utils.is_monday())
