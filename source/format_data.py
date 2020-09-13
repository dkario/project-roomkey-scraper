import pandas as pd


# Reformat SPA col cells: "SPA 1 – Antelope Valley (#1)" -> "Antelope Valley - 1"
def format_spa(df):
    df["SPA"].replace(
        {r"^SPA\s?\d+\s*–?\s*": "", r"\(\D*(\d+)\)$": r"- \1"}, inplace=True, regex=True
    )


# Copy "Total Rooms" col over "Date Operational" col and rename it "# Operational"
# Rename "Service Planning Area (SPA)" col to "SPA"
def rename_cols(df):
    df["Date Operational"] = df["Total Rooms"]
    df.rename(
        columns={
            "Date Operational": "# Operational",
            "Service Planning Area (SPA)": "SPA",
        },
        inplace=True,
    )


# Drop empty columns if scan region is too wide
def trim_cols(df):
    if df.iat[0, 0] == "":
        df.drop(df.columns[0], axis=1, inplace=True)
    if df.iat[0, -1] == "":
        df.drop(df.columns[-1], axis=1, inplace=True)


def format_data(all_tables):
    # Concatenate tables from all pages
    df = pd.concat(all_tables)
    df.reset_index(drop=True, inplace=True)

    # Get columns
    df.columns = df.iloc[0]
    df = df.iloc[1:]

    # Format data
    trim_cols(df)
    rename_cols(df)
    format_spa(df)

    return df
