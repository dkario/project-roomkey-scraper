import tweepy

from source.date_utils import today
from source.get_secret import get_secret
from source.screenshot import get_screenshot_path, screenshot_was_saved_successfully
from tweepy import TweepError


def get_api():
    auth = tweepy.OAuthHandler(
        get_secret("TWITTER_API_KEY"), get_secret("TWITTER_API_SECRET")
    )
    auth.set_access_token(
        get_secret("TWITTER_ACCESS_TOKEN"), get_secret("TWITTER_ACCESS_TOKEN_SECRET")
    )
    api = tweepy.API(auth)
    api.verify_credentials()

    return api


def send_first_tweet_textonly_fallback(text):
    api = get_api()
    tweet = api.update_status(text)

    return tweet


def send_first_tweet_with_screenshot(text, screenshot_path):
    api = get_api()
    tweet = api.update_with_media(screenshot_path, text)

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
        if screenshot_was_saved_successfully():
            daily_totals_tweet = send_first_tweet_with_screenshot(
                format_daily_totals_tweet(daily_totals), get_screenshot_path()
            )
        else:
            daily_totals_tweet = send_first_tweet_textonly_fallback(
                format_daily_totals_tweet(daily_totals)
            )

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
