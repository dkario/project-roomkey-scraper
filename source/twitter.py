import os
import tweepy

from source.date_utils import today
from tweepy import TweepError


def get_api():
    auth = tweepy.OAuthHandler(
        os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET")
    )
    auth.set_access_token(
        os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    api = tweepy.API(auth)
    api.verify_credentials()

    return api


def send_tweet(text):
    api = get_api()
    tweet = api.update_status(text)

    return tweet


def send_reply(text, tweet_id):
    api = get_api()
    tweet = api.update_status(
        text, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True
    )

    return tweet


def format_today():
    return today().strftime("%B %-d")


def format_daily_totals_tweet(daily_totals):
    return """\
Project Roomkey status as of {today}

LOS ANGELES COUNTY
{unsheltered_people}----Unsheltered people
{rooms_promised}----Rooms promised
{rooms_under_contract}-----Rooms under contract
{rooms_operational}-----Rooms operational
{rooms_occupied}-----Rooms occupied

projectroomkeytracker.com""".format(
        today=format_today(),
        unsheltered_people=f"{daily_totals.unsheltered_people:,}",
        rooms_promised=f"{daily_totals.rooms_promised:,}",
        rooms_under_contract=f"{daily_totals.rooms_under_contract:,}",
        rooms_operational=f"{daily_totals.rooms_operational:,}",
        rooms_occupied=f"{daily_totals.rooms_occupied:,}",
    )


def format_data_source_tweet(latest_update_link, page_range):
    start_page, end_page = page_range
    return """\
LA County Data is pulled from the County Emergency Operations Center updates.

Report from {today}:
(Project Roomkey is on pages {start_page}-{end_page})
{latest_update_link}

    """.format(
        today=format_today(),
        start_page=start_page,
        end_page=end_page,
        latest_update_link=latest_update_link,
    )


def send_daily_totals_tweet_thread(daily_totals, page_range, latest_update_link):
    try:
        daily_totals_tweet = send_tweet(format_daily_totals_tweet(daily_totals))
    except TweepError as e:
        if e.args[0][0]["code"] == 187:  # Duplicate tweet
            print("Already tweeted :)")
        else:
            raise e
    else:
        data_source_tweet = send_reply(
            format_data_source_tweet(latest_update_link, page_range),
            daily_totals_tweet.id,
        )

        return daily_totals_tweet
