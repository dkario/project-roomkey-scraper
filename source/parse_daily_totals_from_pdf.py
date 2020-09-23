import pdfplumber

from .daily_totals import DailyTotals
from .exceptions import ScrapeError


def parse_daily_totals_from_pdf(filename):
    with pdfplumber.open(filename) as pdf:
        end_page = [p for p in pdf.pages if "Overall Totals:" in p.extract_text()]

        if not end_page:
            raise ScrapeError("Couldn't find project roomkey data :(")

        words = [word.get("text") for word in end_page[0].extract_words()]

        for i in range(len(words)):
            if words[i] == "Overall" and words[i + 1] == "Totals:":
                rooms_under_contract = words[i + 2]
                rooms_operational = rooms_under_contract
                rooms_occupied = words[i + 3]

                daily_totals = DailyTotals(
                    rooms_under_contract, rooms_operational, rooms_occupied
                )

                return daily_totals

        raise ScrapeError("Couldn't parse project roomkey data :(")
