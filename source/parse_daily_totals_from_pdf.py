import pdfplumber

from .daily_totals import DailyTotals
from .exceptions import ScrapeError

# Return tuple of start and end Page pdfplumber objects
def get_start_and_end_pages(pdf):
    start_page = end_page = None

    for page in pdf.pages:
        text = page.extract_text()
        if "Project Roomkey Locations:" in text:
            start_page = page
        if "Overall Totals:" in text:
            end_page = page

    if start_page is None or end_page is None:
        raise ScrapeError("Couldn't find project roomkey data :(")

    return (start_page, end_page)


def parse_daily_totals_from_pdf(filename):
    with pdfplumber.open(filename) as pdf:
        (start_page, end_page) = get_start_and_end_pages(pdf)

        words = [word.get("text") for word in end_page.extract_words()]

        for i in range(len(words)):
            if words[i] == "Overall" and words[i + 1] == "Totals:":
                rooms_under_contract = words[i + 2]
                rooms_operational = rooms_under_contract
                rooms_occupied = words[i + 3]

                daily_totals = DailyTotals(
                    rooms_under_contract, rooms_operational, rooms_occupied
                )

                return (daily_totals, (start_page.page_number, end_page.page_number))

        raise ScrapeError("Couldn't parse project roomkey data :(")
