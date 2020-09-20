import camelot
import pandas as pd
import pdfplumber

from .exceptions import ScrapeError
from .format_data import format_data, get_daily_totals_from_df

MAX_Y = 792


# Return tuple of start and end Page pdfplumber objects
def get_start_and_end_pages(pdf):
    start_page = end_page = None

    for page in pdf.pages:
        if "Project Roomkey Locations:" in page.extract_text():
            start_page = page
        if "Overall Totals:" in page.extract_text():
            end_page = page

    if start_page is None or end_page is None:
        raise ScrapeError("Couldn't find project roomkey data :(")

    return (start_page, end_page)


# Get the following coordinates for locating tables on all pages
# x_start:      x of table beginning ("Locations:" + 1 word)
# x_end:        x of table end ("Overall Totals" + 3 words)
# y_start:      y of table beginning ("Locations:" + 1 word)
# y_end:        y of table end ("Overall Totals" + 3 words)
# y_page_start: y of new page beginning (first word)
# y_page_end:   of new page end (5th to last word)
def get_coords(start_page, end_page):
    x_start = x_end = y_start = y_end = y_page_start = y_page_end = None

    start_page_words = start_page.extract_words()
    words = list(map(lambda x: x.get("text"), start_page.extract_words()))

    for i in range(len(start_page_words)):
        if (
            words[i] == "Project"
            and words[i + 1] == "Roomkey"
            and words[i + 2] == "Locations:"
        ):
            x_start = start_page_words[i + 3].get("x0") - 5
            y_start = start_page_words[i + 3].get("top")

    y_page_end = start_page_words[-1].get("top") - 18

    end_page_words = end_page.extract_words()
    words = list(map(lambda x: x.get("text"), end_page.extract_words()))

    y_page_start = end_page_words[0].get("top")

    for i in range(len(end_page_words)):
        if words[i] == "Overall" and words[i + 1] == "Totals:":
            x_end = end_page_words[i + 4].get("x1") + 27
            y_end = end_page_words[i + 4].get("bottom")

    coords = (x_start, x_end, y_start, y_end, y_page_start, y_page_end)

    if None in coords:
        raise ScrapeError("Couldn't get table coordinates :(")

    return coords


# Get (x,y) coordinates for top left and bottom right corner of the table on a given page
def get_table_coords(page_number, coords, start_page_number, end_page_number):
    x_start, x_end, y_start, y_end, y_page_start, y_page_end = coords

    x0 = x_start
    y0 = y_start if page_number == start_page_number else y_page_start
    x1 = x_end
    y1 = y_end if page_number == end_page_number else y_page_end

    return (x0, y0, x1, y1)


# Save an image of the table on a given page
def save_table_img(page, table_coords, filename):
    (x0, y0, x1, y1) = table_coords
    cropped = page.crop((x0, y0, x1, y1))
    img = cropped.to_image()
    img.save(str(page.page_number) + "_" + filename[:-4] + ".png", format="PNG")


# Parse data in the table on a given page
def parse_table(page_number, table_coords, filename):
    (x0, y0, x1, y1) = table_coords
    region = ",".join(str(coord) for coord in [x0, MAX_Y - y0, x1, MAX_Y - y1])
    table = camelot.read_pdf(
        filename, pages=str(page_number), table_regions=[region], strip_text="\n"
    )
    return table[0].df


# Export data from all tables to csv
def to_csv(df, filename):
    df.to_csv(filename[:-4] + ".csv", index=False)


# Convert Project Roomkey PDF data to df
def parse_pdf(filename, debug=False):
    with pdfplumber.open(filename) as pdf:
        start_page, end_page = get_start_and_end_pages(pdf)
        start_page_number = start_page.page_number
        end_page_number = end_page.page_number
        coords = get_coords(start_page, end_page)
        roomkey_pages = pdf.pages[start_page_number - 1 : end_page_number]

        all_tables = []

        for page in roomkey_pages:
            page_number = page.page_number
            table_coords = get_table_coords(
                page_number, coords, start_page_number, end_page_number
            )

            if debug:
                save_table_img(page, table_coords, filename)

            all_tables.append(parse_table(page_number, table_coords, filename))

        df = format_data(all_tables)

        return df


def get_daily_totals(filename, debug=False):
    # Uncomment to bypass parsing pdf and test quickly with saved data
    # csv_filename = "8.21.20_COVID-19_Update_FINAL.csv"
    # df = read_csv(csv_filename)

    df = parse_pdf(filename, debug)

    if debug:
        to_csv(df, filename)

    return get_daily_totals_from_df(df)
