import os
import tweepy
from datetime import date


def get_api():
    auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth)
    api.verify_credentials()

    return api


def send_tweet(text):
    api = get_api()
    tweet = api.update_status(text)

    return tweet


def format_daily_totals_tweet(daily_totals):
    today = date.today().strftime("%B %-d")

    return """\
Project Roomkey status as of {today}

LOS ANGELES COUNTY
{unsheltered_people}----Unsheltered people
{rooms_promised}----Rooms promised
{rooms_under_contract}-----Rooms under contract
{rooms_operational}-----Rooms operational
{rooms_occupied}-----Rooms occupied\
    """.format(
        today=today,
        **vars(daily_totals),
    )


def send_daily_totals_tweet(daily_totals):
    tweet = format_daily_totals_tweet(daily_totals)

    return send_tweet(tweet)
