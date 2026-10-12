import csv
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pandas as pd

from data_loader import CSVValidationError, load_campaign_csv

ROOT = Path(__file__).resolve().parents[1]


def sample_rows():
    return [
        dict(date="2026-04-01", campaign_id="001", campaign_name="Test A", channel="Facebook",
             audience="Prospecting", goal="Sales", impressions="1000", clicks="100",
             conversions="10", spend="200.00", revenue="600.00", currency="USD", dataset_type="synthetic"),
        dict(date="2026-04-02", campaign_id="002", campaign_name="Test B", channel="Instagram",
             audience="Retargeting", goal="Traffic", impressions="500", clicks="50",
             conversions="0", spend="100.00", revenue="0.00", currency="USD", dataset_type="synthetic"),
    ]


def encode_csv(rows):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


class LoaderTests(unittest.TestCase):
    def test_both_supplied_files_match_and_reconcile(self):
        original = load_campaign_csv((ROOT / "campaign_data_synthetic.csv").read_bytes())
        compatible = load_campaign_csv((ROOT / "campaign_data_synthetic_compatible.csv").read_bytes())
        pd.testing.assert_frame_equal(original.data, compatible.data)
        self.assertEqual(compatible.mapped_headers, ["campaign_goal → goal", "data_source → dataset_type"])
        self.assertEqual(len(original.data), 4040)
        self.assertEqual(original.data.campaign_id.nunique(), 24)
        self.assertEqual(original.data.date.nunique(), 183)
        self.assertAlmostEqual(original.data.spend.sum(), 306470.04, places=2)
        self.assertAlmostEqual(original.data.revenue.sum(), 839690.13, places=2)
        self.assertEqual(original.data.conversions.sum(), 7823)
        self.assertFalse(original.warnings)

    def test_identifiers_extra_columns_and_header_normalization(self):
        rows = sample_rows()
        for row in rows:
            row["extra_note"] = "Keep me"
        payload = encode_csv(rows).replace(b"date,campaign_id", b" DATE , CAMPAIGN_ID ")
        loaded = load_campaign_csv(b"\xef\xbb\xbf" + payload)
        self.assertEqual(loaded.data.campaign_id.iloc[0], "001")
        self.assertEqual(set(loaded.data.extra_note), {"Keep me"})

    def test_missing_revenue_is_unknown_and_zero_is_preserved(self):
        for missing in ["", "N/A", "NaN", "null"]:
            with self.subTest(missing=missing):
                rows = sample_rows()
                rows[0]["revenue"] = missing
                loaded = load_campaign_csv(encode_csv(rows))
                self.assertTrue(pd.isna(loaded.data.revenue.iloc[0]))
                self.assertEqual(loaded.data.revenue.iloc[1], 0)
                self.assertIn("1 of 2", loaded.warnings[0])
        rows = [{k: v for k, v in r.items() if k != "revenue"} for r in sample_rows()]
        loaded = load_campaign_csv(encode_csv(rows))
        self.assertTrue(loaded.data.revenue.isna().all())
        self.assertIn("2 of 2", loaded.warnings[0])

    def test_zero_activity_and_credit_funded_day_are_valid(self):
        rows = sample_rows()
        for col in ["impressions", "clicks", "conversions", "spend", "revenue"]:
            rows[0][col] = "0"
        rows[1].update(impressions="1000", clicks="10", conversions="2", spend="0", revenue="190")
        loaded = load_campaign_csv(encode_csv(rows))
        self.assertEqual(len(loaded.data), 2)
        self.assertEqual(loaded.data.spend.sum(), 0)
        self.assertEqual(loaded.data.revenue.sum(), 190)

    def test_invalid_required_fields_are_rejected(self):
        for column, value in [
            ("date", "2026-02-30"), ("date", "2026-4-1"),
            ("campaign_id", " "), ("campaign_name", ""), ("audience", ""),
            ("impressions", "10.5"), ("impressions", "oops"), ("impressions", str(2**53)),
            ("clicks", "1001"), ("conversions", "101"),
            ("spend", ""), ("spend", "-1"), ("spend", "inf"), ("spend", "NaN"),
            ("revenue", "-1"), ("revenue", "inf"), ("revenue", "unknown text"),
            ("currency", "DOLLARS"),
        ]:
            with self.subTest(column=column, value=value):
                rows = sample_rows()
                rows[0][column] = value
                with self.assertRaises(CSVValidationError):
                    load_campaign_csv(encode_csv(rows))

    def test_duplicates_currency_and_metadata_conflicts(self):
        rows = sample_rows()
        cases = [
            ([rows[0], rows[0]], "same date"),
            ([rows[0], {**rows[1], "currency": "EUR"}], "Multiple currencies"),
            ([rows[0], {**rows[1], "campaign_id": "001"}], "inconsistent"),
        ]
        for data, expected in cases:
            with self.subTest(expected=expected), self.assertRaisesRegex(CSVValidationError, expected):
                load_campaign_csv(encode_csv(data))

    def test_missing_provenance_is_not_labelled_real(self):
        rows = [{k: v for k, v in r.items() if k != "dataset_type"} for r in sample_rows()]
        loaded = load_campaign_csv(encode_csv(rows))
        self.assertEqual(set(loaded.data.dataset_type), {"unspecified"})

    def test_invalid_csv_structure_and_ambiguous_headers(self):
        good = encode_csv(sample_rows())
        cases = [b"", b"\xff", b"date,date\n", b"ticker,shares\nABC,2\n",
                 good.split(b"\r\n")[0] + b"\n", good + b"bad,row\n",
                 good + b"\n", good + b'"unclosed quote\n']
        for payload in cases:
            with self.subTest(payload=payload[:30]), self.assertRaises(CSVValidationError):
                load_campaign_csv(payload)
        rows = sample_rows()
        for row in rows:
            row["campaign_goal"] = row["goal"]
        with self.assertRaisesRegex(CSVValidationError, "either goal"):
            load_campaign_csv(encode_csv(rows))

    def test_file_and_row_limits(self):
        with patch("data_loader.MAX_UPLOAD_BYTES", 1), self.assertRaisesRegex(CSVValidationError, "too large"):
            load_campaign_csv(encode_csv(sample_rows()))
        with patch("data_loader.MAX_ROWS", 1), self.assertRaisesRegex(CSVValidationError, "too many"):
            load_campaign_csv(encode_csv(sample_rows()))


if __name__ == "__main__":
    unittest.main()
