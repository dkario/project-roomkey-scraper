import gspread
import json
import os
import boto3
import base64

from botocore.exceptions import ClientError
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from source.daily_totals import DailyTotals
from source.date_utils import get_days_ago, is_monday, today


def get_api():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    if os.getenv("ENVIRONMENT") == "dev":
        with open("./google_credentials.json", "r") as credentials_file:
            credentials = Credentials.from_service_account_info(
                json.load(credentials_file), scopes=scopes
            )
    else:
        credentials = Credentials.from_service_account_info(
            get_google_account_credentials_secret(), scopes=scopes
        )

    return gspread.authorize(credentials)


def get_google_account_credentials_secret():
    secret_name = os.getenv("GOOGLE_CREDENTIALS")

    ssm = boto3.client("ssm")
    secret = ssm.get_parameter(Name=secret_name, WithDecryption=True)["Parameter"][
        "Value"
    ]

    return json.loads(secret)


def get_LAC_data_worksheet():
    gc = get_api()
    sheet = gc.open_by_key(os.getenv("GOOGLE_SHEET_ID"))
    return sheet.get_worksheet(0)  # "LAC Data"


def format_date(date):
    return date.strftime("%-m/%-d/%Y")


def copy_last_friday_values_through_weekend():
    worksheet = get_LAC_data_worksheet()
    last_row = get_LAC_data_worksheet().get_all_values()[-1]
    last_row_without_date = last_row[1:]
    saturday = format_date(get_days_ago(2))
    sunday = format_date(get_days_ago(1))

    worksheet.append_row([saturday] + last_row_without_date)
    worksheet.append_row([sunday] + last_row_without_date)


def append_daily_totals(daily_totals):
    get_LAC_data_worksheet().append_row(
        [
            format_date(today()),
            daily_totals.rooms_promised,
            daily_totals.rooms_under_contract,
            daily_totals.rooms_operational,
            daily_totals.rooms_occupied,
            daily_totals.people_in_rooms,
        ]
    )


def update_google_sheet(daily_totals):
    if is_monday():
        copy_last_friday_values_through_weekend()

    append_daily_totals(daily_totals)


def main():
    load_dotenv()

    daily_totals = DailyTotals(100, 200, 300, 400)
    update_google_sheet(daily_totals)


if __name__ == "__main__":
    main()
