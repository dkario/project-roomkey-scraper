import unittest
import pandas as pd

import source.format_data as format_data


class TestFormatData(unittest.TestCase):
    def test_format_spa(self):
        df = pd.DataFrame(
            {
                "SPA": [
                    "SPA 1 – Antelope Valley (#1)",
                    "SPA 3 San Gabriel Valley (#1)",
                    "SPA 2 – San Fernando Valley (# 1)",
                    "SPA 7– East (#3)",
                    "SPA 6 –South (#2)",
                ]
            }
        )
        format_data.format_spa(df)

        pd.testing.assert_frame_equal(
            df,
            pd.DataFrame(
                {
                    "SPA": [
                        "Antelope Valley - 1",
                        "San Gabriel Valley - 1",
                        "San Fernando Valley - 1",
                        "East - 3",
                        "South - 2",
                    ]
                }
            ),
        )

    def test_rename_cols(self):
        df = pd.DataFrame(
            {
                "Service Planning Area (SPA)": [],
                "Total Rooms": [],
                "Date Operational": [],
                "# of Rooms Occupied": [],
                "# of Clients": [],
            }
        )
        format_data.rename_cols(df)

        pd.testing.assert_frame_equal(
            df,
            pd.DataFrame(
                {
                    "SPA": [],
                    "Total Rooms": [],
                    "# Operational": [],
                    "# of Rooms Occupied": [],
                    "# of Clients": [],
                }
            ),
        )

    def test_trim_cols(self):
        df = pd.DataFrame(
            {
                "": [""],
                "Service Planning Area (SPA)": ["SPA 1 – Antelope Valley (#1)"],
                "Total Rooms": ["10"],
                "Date Operational": ["4/6/2020"],
                "# of Rooms Occupied": ["9"],
                "# of Clients": ["12"],
                "": [""],
            }
        )
        format_data.trim_cols(df)

        pd.testing.assert_frame_equal(
            df,
            pd.DataFrame(
                {
                    "Service Planning Area (SPA)": ["SPA 1 – Antelope Valley (#1)"],
                    "Total Rooms": ["10"],
                    "Date Operational": ["4/6/2020"],
                    "# of Rooms Occupied": ["9"],
                    "# of Clients": ["12"],
                }
            ),
        )
