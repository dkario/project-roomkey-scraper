from dotenv import load_dotenv
from pandas import read_csv

from .twitter import send_daily_totals_tweet
from .read_pdf import get_daily_totals
from .format_data import DailyTotals


def main():
    filename = "9.17.20_COVID-19_Update_FINAL.pdf"
    load_dotenv()

    daily_totals = get_daily_totals(filename)
    send_daily_totals_tweet(daily_totals)


if __name__ == "__main__":
    main()
