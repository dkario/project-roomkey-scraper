import unittest
import pandas as pd

import source.read_pdf as read_pdf


class TestReadPdf(unittest.TestCase):
    # Output of get_table_coords is a 4-tuple representing (x0, y0, x1, y1)
    def test_get_table_coords(self):
        # x_start, x_end, y_start, y_end, y_page_start, y_page_end
        test_coords = (1, 2, 3, 4, 5, 6)

        # When page_number equals start_page_number, y0 should be y_start
        # When page_number equals end_page_number, y1 should be y_end
        self.assertEqual(
            read_pdf.get_table_coords(
                page_number=0,
                coords=test_coords,
                start_page_number=0,
                end_page_number=0,
            ),
            (1, 3, 2, 4),
        )

        # When page_number doesn't equal start_page_number, y0 should be y_page_start
        self.assertEqual(
            read_pdf.get_table_coords(
                page_number=1,
                coords=test_coords,
                start_page_number=0,
                end_page_number=1,
            ),
            (1, 5, 2, 4),
        )

        # When page_number doesn't equal end_page_number, y1 should be y_page_end
        self.assertEqual(
            read_pdf.get_table_coords(
                page_number=0,
                coords=test_coords,
                start_page_number=0,
                end_page_number=1,
            ),
            (1, 3, 2, 6),
        )
