from dotenv import load_dotenv

from source.google_sheets import update_google_sheet
from source.parse_daily_totals_from_pdf import parse_daily_totals_from_pdf
from source.scrape_roomkey import save_latest_incident_update_from_project_roomkey_site
from source.screenshot import take_screenshot_of_website_graph
from source.twitter import send_daily_totals_tweet_thread


def main():
    load_dotenv()

    (filename, link) = save_latest_incident_update_from_project_roomkey_site()
    (daily_totals, page_range) = parse_daily_totals_from_pdf(filename)
    update_google_sheet(daily_totals)
    take_screenshot_of_website_graph()
    send_daily_totals_tweet_thread(daily_totals, page_range, link)


if __name__ == "__main__":
    main()
