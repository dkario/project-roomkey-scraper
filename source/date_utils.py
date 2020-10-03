# This file returns date objects that have 1 day subtracted. We do this because
# the cron runs on Tuesdays at 3AM UTC, which is Mondays at 8pm PT, and we want
# to display dates in PT.

import os

from datetime import date, timedelta
from dotenv import load_dotenv


def get_day_offset():
    load_dotenv()

    return int(os.getenv("DAY_OFFSET"))  # 0 when run locally, 1 when run in the cron


def actually_today():
    return date.today()


def today():
    return actually_today() - timedelta(days=0 + get_day_offset())


def is_monday():
    # 0 corresponds to Monday, 1 corresponds to Tuesday
    return actually_today().weekday() == (0 + get_day_offset())


def get_days_ago(days_ago):
    return actually_today() - timedelta(days=days_ago + get_day_offset())
