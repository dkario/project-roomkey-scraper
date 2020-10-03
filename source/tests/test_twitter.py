import unittest
from unittest.mock import Mock

import source.twitter as twitter
from source.daily_totals import DailyTotals


class TestTwitter(unittest.TestCase):
    def test_format_daily_totals_tweet(self):
        twitter.format_today = Mock()
        twitter.format_today.return_value = "January 1"

        daily_totals = DailyTotals(1000, 2000, 3000, 4000)
        expected = """\
Project Roomkey status as of January 1

LOS ANGELES COUNTY
48,038----Unsheltered people
15,000----Rooms promised
1,000-----Rooms under contract
2,000-----Rooms operational
3,000-----Rooms occupied

projectroomkeytracker.com"""

        self.assertEqual(twitter.format_daily_totals_tweet(daily_totals), expected)
