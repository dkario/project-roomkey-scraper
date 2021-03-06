import gspread

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from source.daily_totals import DailyTotals
from source.date_utils import get_days_ago, is_monday, today
from source.get_secret import get_secret


def get_api():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    credentials = Credentials.from_service_account_info(
        get_secret("GOOGLE_CREDENTIALS", is_json=True), scopes=scopes
    )

    return gspread.authorize(credentials)


def get_LAC_data_worksheet():
    gc = get_api()
    sheet = gc.open_by_key(get_secret("GOOGLE_SHEET_ID"))

    return sheet.get_worksheet(0)  # "LAC Data"


def format_date(date):
    return date.strftime("%-m/%-d/%Y")


def copy_last_friday_values_through_weekend():
    worksheet = get_LAC_data_worksheet()
    last_row = get_LAC_data_worksheet().get_all_values()[-1]
    last_row_without_date = last_row[1:]
    saturday = format_date(get_days_ago(2))
    sunday = format_date(get_days_ago(1))

    worksheet.append_row(
        [saturday] + last_row_without_date, value_input_option="USER_ENTERED"
    )
    worksheet.append_row(
        [sunday] + last_row_without_date, value_input_option="USER_ENTERED"
    )


def append_daily_totals(daily_totals):
    get_LAC_data_worksheet().append_row(
        [
            format_date(today()),
            daily_totals.rooms_promised,
            daily_totals.rooms_under_contract,
            daily_totals.rooms_operational,
            daily_totals.rooms_occupied,
            daily_totals.people_in_rooms,
        ],
        value_input_option="USER_ENTERED",
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
