from dotenv import load_dotenv
from pandas import read_csv

from source.twitter import send_daily_totals_tweet
from source.read_pdf import get_daily_totals
from source.format_data import DailyTotals
from source.scrape_roomkey import save_latest_incident_update_from_project_roomkey_site


def main():
    load_dotenv()

    pdf_filename = save_latest_incident_update_from_project_roomkey_site()
    daily_totals = get_daily_totals(pdf_filename)
    send_daily_totals_tweet(daily_totals)


if __name__ == "__main__":
    main()
