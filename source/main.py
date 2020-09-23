from dotenv import load_dotenv

from source.twitter import send_daily_totals_tweet
from source.parse_daily_totals_from_pdf import parse_daily_totals_from_pdf
from source.scrape_roomkey import save_latest_incident_update_from_project_roomkey_site


def main():
    load_dotenv()

    pdf_filename = save_latest_incident_update_from_project_roomkey_site()
    daily_totals = parse_daily_totals_from_pdf(pdf_filename)
    send_daily_totals_tweet(daily_totals)


if __name__ == "__main__":
    main()
