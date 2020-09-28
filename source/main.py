from dotenv import load_dotenv

from source.twitter import send_daily_totals_tweet_thread
from source.parse_daily_totals_from_pdf import parse_daily_totals_from_pdf
from source.scrape_roomkey import save_latest_incident_update_from_project_roomkey_site


def main():
    load_dotenv()

    (filename, link) = save_latest_incident_update_from_project_roomkey_site()
    (daily_totals, page_range) = parse_daily_totals_from_pdf(filename)
    send_daily_totals_tweet_thread(daily_totals, page_range, link)


if __name__ == "__main__":
    main()
