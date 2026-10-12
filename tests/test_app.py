import base64
import json
import struct
import unittest
from datetime import date
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class Upload(BytesIO):
    def __init__(self, contents, name):
        super().__init__(contents)
        self.name = name


class AppTests(unittest.TestCase):
    def app(self):
        return AppTest.from_file(str(ROOT / "app.py"), default_timeout=20).run()

    def upload(self, contents, name):
        app = self.app()
        app.radio[0].set_value("Upload CSV")
        # Drive the app's real upload branch with UploadedFile-compatible bytes.
        # OS file-picker interaction remains a manual check.
        with patch("streamlit.file_uploader", return_value=Upload(contents, name)):
            app.run()
        return app

    def test_demo_preview(self):
        app = self.app()
        self.assertFalse(app.exception)
        self.assertIn("4,040 rows", app.success[0].value)
        self.assertEqual(len(app.dataframe[0].value), 50)
        self.assertIn("Synthetic", app.warning[0].value)
        app.selectbox[0].set_value(10).run()
        self.assertEqual(len(app.dataframe[0].value), 10)

    def test_upload_without_file_has_no_stale_preview(self):
        app = self.app()
        app.radio[0].set_value("Upload CSV").run()
        self.assertFalse(app.exception)
        self.assertIn("Choose a campaign CSV", app.info[0].value)
        self.assertEqual(len(app.dataframe), 0)
        self.assertEqual(len(app.success), 0)

    def test_original_and_compatible_uploads(self):
        for name in ["campaign_data_synthetic.csv", "campaign_data_synthetic_compatible.csv"]:
            with self.subTest(name=name):
                app = self.upload((ROOT / name).read_bytes(), name)
                self.assertFalse(app.exception)
                self.assertIn("4,040 rows", app.success[0].value)
                self.assertEqual(len(app.dataframe[0].value), 50)
                self.assertIn("goal", app.dataframe[0].value.columns)

    def test_invalid_upload_has_error_and_no_stale_data(self):
        app = self.upload(b"ticker,shares\nABC,2\n", "invalid.csv")
        self.assertFalse(app.exception)
        self.assertIn("Missing required columns", app.error[0].value)
        self.assertEqual(len(app.dataframe), 0)
        self.assertEqual(len(app.success), 0)

    def test_missing_revenue_warning_in_real_app_path(self):
        from test_data_loader import encode_csv, sample_rows
        rows = sample_rows()
        rows[0]["revenue"] = ""
        app = self.upload(encode_csv(rows), "missing_revenue.csv")
        self.assertFalse(app.exception)
        self.assertTrue(any("Revenue is missing in 1 of 2" in w.value for w in app.warning))
        self.assertTrue(app.dataframe[0].value.revenue.isna().iloc[0])
        self.assertEqual(app.dataframe[0].value.revenue.iloc[1], 0)
        self.assertEqual(app.metric[1].value, "N/A")
        self.assertEqual(app.metric[5].value, "N/A")
        app.multiselect[0].set_value(["Instagram"])
        with patch("streamlit.file_uploader", return_value=Upload(encode_csv(rows), "missing_revenue.csv")):
            app.run()
        self.assertEqual(app.metric[1].value, "0.00")
        self.assertEqual(app.metric[5].value, "0.00×")
        self.assertFalse(any("selected rows" in w.value for w in app.warning))

    def test_overview_baseline_and_real_chart_data(self):
        app = self.app()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric], ["306,470.04", "839,690.13", "7,823", "1.45%", "39.18", "2.74×"])
        self.assertEqual(len(app.get("plotly_chart")), 2)
        self.assertAlmostEqual(self.chart_spend(app), 306470.04, places=2)

    @staticmethod
    def chart_values(app, axis="x", chart_index=0, trace_index=0):
        chart = json.loads(app.get("plotly_chart")[chart_index].proto.spec)
        values = chart["data"][trace_index][axis]
        if isinstance(values, dict):
            packed = base64.b64decode(values["bdata"])
            dtype = {"f8": "d", "f4": "f", "i8": "q", "i4": "i", "i2": "h", "i1": "b",
                     "u8": "Q", "u4": "I", "u2": "H", "u1": "B"}[values["dtype"]]
            values = struct.unpack("<" + dtype * (len(packed) // struct.calcsize(dtype)), packed)
        return list(values)

    @staticmethod
    def chart_spend(app):
        return sum(AppTests.chart_values(app))

    def test_four_filters_update_cards_chart_table_and_reset(self):
        app = self.app()
        app.date_input[0].set_value(date(2026, 6, 1))
        app.date_input[1].set_value(date(2026, 6, 30))
        app.multiselect[0].set_value(["Instagram"])
        app.multiselect[1].set_value(["Prospecting"])
        app.multiselect[2].set_value(["Sales"])
        app.selectbox[0].set_value(100)
        app.run()
        self.assertFalse(app.exception)
        selected = app.dataframe[0].value
        self.assertEqual(len(selected), 60)
        self.assertEqual(selected.campaign_id.nunique(), 2)
        self.assertEqual(set(selected.channel), {"Instagram"})
        self.assertEqual(set(selected.audience), {"Prospecting"})
        self.assertEqual(set(selected.goal), {"Sales"})
        self.assertEqual([m.value for m in app.metric], ["9,394.52", "20,205.07", "175", "1.46%", "53.68", "2.15×"])
        self.assertAlmostEqual(selected.spend.sum(), 9394.52, places=2)
        self.assertAlmostEqual(self.chart_spend(app), selected.spend.sum(), places=2)
        self.assertAlmostEqual(sum(self.chart_values(app, "y", 1, 0)), 9394.52, places=2)
        self.assertEqual(sum(self.chart_values(app, "y", 1, 1)), 175)
        self.assertEqual(len(self.chart_values(app, "x", 1, 0)), 30)
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, "306,470.04")
        self.assertEqual(len(app.multiselect[0].value), 4)
        # The browser must receive a value update, not just recalculated backend totals.
        self.assertTrue(app.multiselect[0].proto.set_value)
        self.assertEqual(list(app.multiselect[0].proto.raw_values), ["Facebook", "Instagram", "Pinterest", "Twitter"])
        self.assertEqual(app.date_input[0].value, date(2026, 4, 1))

    def test_empty_selection_and_invalid_date_range_hide_results(self):
        app = self.app()
        app.multiselect[0].set_value([]).run()
        self.assertFalse(app.exception)
        self.assertIn("No rows match", app.info[0].value)
        self.assertEqual(len(app.metric), 0)
        self.assertEqual(len(app.dataframe), 0)
        self.assertEqual(len(app.get("plotly_chart")), 0)
        app = self.app()
        app.date_input[0].set_value(date(2026, 9, 30))
        app.date_input[1].set_value(date(2026, 4, 1))
        app.run()
        self.assertFalse(app.exception)
        self.assertIn("Start date", app.error[0].value)
        self.assertEqual(len(app.metric), 0)

    def test_credit_funded_record_shows_zero_cost_and_na_roas(self):
        from test_data_loader import encode_csv, sample_rows
        row = sample_rows()[0]
        row.update(impressions="1000", clicks="10", conversions="2", spend="0", revenue="190")
        app = self.upload(encode_csv([row]), "credit_funded.csv")
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric], ["0.00", "190.00", "2", "1.00%", "0.00", "N/A"])

    def test_new_file_contents_get_fresh_filter_defaults(self):
        from test_data_loader import encode_csv, sample_rows
        app = self.app()
        app.multiselect[0].set_value(["Instagram"]).run()
        rows = sample_rows()[:1]  # Only Facebook exists in this upload.
        app.radio[0].set_value("Upload CSV")
        with patch("streamlit.file_uploader", return_value=Upload(encode_csv(rows), "new.csv")):
            app.run()
        self.assertFalse(app.exception)
        self.assertEqual(app.multiselect[0].value, ["Facebook"])
        self.assertEqual(app.metric[0].value, "200.00")

    def test_platform_controls_and_metric_selection(self):
        controls = json.loads((ROOT / "DATA_INSPECTION.json").read_text())
        app = self.app()
        app.radio[1].set_value("Platform Comparison").run()
        self.assertFalse(app.exception)
        comparison = app.dataframe[0].value
        self.assertEqual(len(comparison), 4)
        for _, row in comparison.iterrows():
            reference = controls["by_channel"][row.channel]
            for field in ["spend", "revenue", "conversions", "ctr_pct", "cpa", "roas"]:
                self.assertAlmostEqual(row[field], float(reference[field]), places=7)
        self.assertEqual(app.metric[0].value, "306,470.04")
        self.assertAlmostEqual(self.chart_spend(app), comparison.spend.sum(), places=2)
        app.selectbox[0].set_value("ROAS").run()
        expected = sorted(v["roas"] for v in controls["by_channel"].values())
        for actual, reference in zip(sorted(self.chart_values(app)), expected):
            self.assertAlmostEqual(actual, reference)
        app.selectbox[0].set_value("Purchases").run()
        self.assertEqual(sum(self.chart_values(app)), 7823)

    def test_shared_filters_persist_across_all_four_views(self):
        app = self.app()
        app.date_input[0].set_value(date(2026, 6, 1))
        app.date_input[1].set_value(date(2026, 6, 30))
        app.multiselect[0].set_value(["Instagram"])
        app.multiselect[1].set_value(["Prospecting"])
        app.multiselect[2].set_value(["Sales"])
        app.run()
        app.radio[1].set_value("Platform Comparison").run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.dataframe[0].value), 1)
        self.assertEqual(app.metric[0].value, "9,394.52")
        self.assertAlmostEqual(app.dataframe[0].value.spend.iloc[0], 9394.52, places=2)
        app.radio[1].set_value("Campaign Details").run()
        self.assertFalse(app.exception)
        campaigns = app.dataframe[0].value
        self.assertEqual(set(campaigns.campaign_id), {"CMP007", "CMP010"})
        self.assertAlmostEqual(campaigns.spend.sum(), 9394.52, places=2)
        self.assertAlmostEqual(campaigns.revenue.sum(), 20205.07, places=2)
        self.assertEqual(campaigns.conversions.sum(), 175)
        app.selectbox[0].set_value("CMP010").run()
        daily = app.dataframe[1].value
        self.assertEqual(len(daily), 30)
        self.assertEqual(set(daily.campaign_id), {"CMP010"})
        self.assertEqual(set(daily.channel), {"Instagram"})
        self.assertEqual(set(daily.audience), {"Prospecting"})
        self.assertEqual(set(daily.goal), {"Sales"})
        self.assertEqual(daily.date.min(), "2026-06-01")
        self.assertEqual(daily.date.max(), "2026-06-30")
        self.assertEqual(app.metric[0].value, f"{daily.spend.sum():,.2f}")
        self.assertEqual(app.metric[5].value, f"{daily.revenue.sum() / daily.spend.sum():.2f}×")
        app.radio[1].set_value("Time Series").run()
        self.assertFalse(app.exception)
        periods = app.dataframe[0].value
        self.assertEqual(len(periods), 30)
        self.assertEqual(periods.recorded_rows.sum(), 60)
        self.assertAlmostEqual(periods.spend.sum(), 9394.52, places=2)
        self.assertAlmostEqual(sum(self.chart_values(app, "y")), 9394.52, places=2)
        self.assertEqual(app.metric[0].value, "9,394.52")
        app.radio[1].set_value("Overview").run()
        self.assertEqual(app.metric[0].value, "9,394.52")
        self.assertEqual(app.multiselect[0].value, ["Instagram"])
        self.assertEqual(app.date_input[0].value, date(2026, 6, 1))

    def test_campaign_search_is_case_insensitive_literal_and_clearable(self):
        app = self.app()
        app.radio[1].set_value("Campaign Details").run()
        self.assertEqual(len(app.dataframe[0].value), 24)
        app.text_input[0].set_value("summer LAUNCH").run()
        self.assertFalse(app.exception)
        self.assertEqual(set(app.dataframe[0].value.campaign_id), {"CMP004", "CMP010", "CMP016", "CMP022"})
        app.text_input[0].set_value("cmp010").run()
        self.assertEqual(app.selectbox[0].value, "CMP010")
        self.assertEqual(len(app.dataframe[0].value), 1)
        self.assertEqual(set(app.dataframe[1].value.campaign_id), {"CMP010"})
        app.text_input[0].set_value("[").run()  # Treated as text, not an invalid regex.
        self.assertFalse(app.exception)
        self.assertTrue(any("No campaigns match" in info.value for info in app.info))
        self.assertEqual(len(app.metric), 0)
        self.assertEqual(len(app.dataframe), 0)
        app.text_input[0].set_value("").run()
        self.assertEqual(len(app.dataframe[0].value), 24)

    def test_campaign_selection_cannot_restore_excluded_records(self):
        app = self.app()
        app.radio[1].set_value("Campaign Details").run()
        app.selectbox[0].set_value("CMP010").run()
        app.multiselect[0].set_value(["Facebook"]).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox[0].value, "CMP001")
        self.assertEqual(set(app.dataframe[0].value.channel), {"Facebook"})
        self.assertEqual(set(app.dataframe[1].value.channel), {"Facebook"})
        self.assertNotIn("CMP010", app.dataframe[0].value.campaign_id.values)

    def test_platform_unknown_and_zero_revenue_are_distinct(self):
        from test_data_loader import encode_csv, sample_rows
        rows = sample_rows()
        rows[0]["revenue"] = ""
        contents = encode_csv(rows)
        app = self.upload(contents, "missing.csv")
        with patch("streamlit.file_uploader", return_value=Upload(contents, "missing.csv")):
            app.radio[1].set_value("Platform Comparison").run()
            app.selectbox[0].set_value("ROAS").run()
        comparison = app.dataframe[0].value
        self.assertTrue(comparison.loc[comparison.channel.eq("Facebook"), "revenue"].isna().all())
        self.assertEqual(comparison.loc[comparison.channel.eq("Instagram"), "roas"].iloc[0], 0)
        self.assertEqual(self.chart_values(app), [0])
        self.assertTrue(any("1 channel has unavailable ROAS" in info.value for info in app.info))
        for row in rows:
            row["revenue"] = ""
        contents = encode_csv(rows)
        with patch("streamlit.file_uploader", return_value=Upload(contents, "all_missing.csv")):
            app.run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.get("plotly_chart")), 0)
        self.assertEqual(len(app.dataframe[0].value), 2)
        self.assertTrue(any("every selected channel" in info.value for info in app.info))

    def test_campaign_missing_revenue_is_scoped_to_selected_campaign(self):
        from test_data_loader import encode_csv, sample_rows
        rows = sample_rows()
        rows[0]["revenue"] = ""
        contents = encode_csv(rows)
        app = self.upload(contents, "missing.csv")
        with patch("streamlit.file_uploader", return_value=Upload(contents, "missing.csv")):
            app.radio[1].set_value("Campaign Details").run()
            self.assertEqual(app.metric[1].value, "N/A")
            app.selectbox[0].set_value("002").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[1].value, "0.00")
        self.assertEqual(app.metric[5].value, "0.00×")
        self.assertFalse(any("selected rows" in warning.value for warning in app.warning))

    def test_empty_shared_filters_hide_results_in_new_views(self):
        for view in ["Platform Comparison", "Campaign Details", "Time Series"]:
            with self.subTest(view=view):
                app = self.app()
                app.radio[1].set_value(view)
                app.multiselect[0].set_value([]).run()
                self.assertFalse(app.exception)
                self.assertEqual(len(app.metric), 0)
                self.assertEqual(len(app.dataframe), 0)
                self.assertEqual(len(app.get("plotly_chart")), 0)
                self.assertTrue(any("No rows match" in info.value for info in app.info))

    def test_negative_ad_spend_returns_have_an_honest_axis(self):
        from test_data_loader import encode_csv, sample_rows
        contents = encode_csv(sample_rows())
        app = self.upload(contents, "returns.csv")
        with patch("streamlit.file_uploader", return_value=Upload(contents, "returns.csv")):
            app.radio[1].set_value("Platform Comparison").run()
            app.selectbox[0].set_value("Ad-spend return").run()
        self.assertFalse(app.exception)
        self.assertEqual(sorted(self.chart_values(app)), [-100, 200])
        spec = json.loads(app.get("plotly_chart")[0].proto.spec)
        limits = spec["layout"]["xaxis"]["range"]
        self.assertLessEqual(limits[0], -100)
        self.assertGreaterEqual(limits[1], 200)

    def test_time_series_daily_weekly_and_metric_encodings(self):
        app = self.app()
        app.radio[1].set_value("Time Series").run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.dataframe[0].value), 183)
        self.assertAlmostEqual(sum(self.chart_values(app, "y")), 306470.04, places=2)
        app.selectbox[0].set_value("Weekly").run()
        periods = app.dataframe[0].value
        self.assertEqual(len(periods), 27)
        self.assertEqual(periods.partial_week.sum(), 2)
        self.assertEqual(periods.recorded_rows.sum(), 4040)
        self.assertAlmostEqual(sum(self.chart_values(app, "y")), 306470.04, places=2)
        app.selectbox[1].set_value("ROAS").run()
        for actual, (_, row) in zip(self.chart_values(app, "y"), periods.iterrows()):
            self.assertAlmostEqual(actual, row.revenue / row.spend)
        app.selectbox[1].set_value("Clicks").run()
        self.assertEqual(sum(self.chart_values(app, "y")), 437337)

    def test_overview_paired_trend_reconciles_and_uses_separate_units(self):
        app = self.app()
        spend = self.chart_values(app, "y", 1, 0)
        purchases = self.chart_values(app, "y", 1, 1)
        self.assertEqual(len(spend), 183)
        self.assertAlmostEqual(sum(spend), 306470.04, places=2)
        self.assertEqual(sum(purchases), 7823)
        self.assertEqual(self.chart_values(app, "x", 1, 0), self.chart_values(app, "x", 1, 1))
        spec = json.loads(app.get("plotly_chart")[1].proto.spec)
        self.assertEqual(spec["layout"]["yaxis"]["title"]["text"], "Spend (USD)")
        self.assertEqual(spec["layout"]["yaxis2"]["title"]["text"], "Conversions (purchases)")
        self.assertEqual(spec["layout"]["xaxis"]["matches"], "x2")
        for trace in spec["data"]:
            self.assertFalse(trace["connectgaps"])
            self.assertIn("markers", trace["mode"])

    def test_overview_trend_preserves_absent_dates_and_recorded_zeros(self):
        import math
        from test_data_loader import encode_csv, sample_rows
        rows = sample_rows()
        rows[1].update(date="2026-04-03", impressions="0", clicks="0", conversions="0", spend="0", revenue="0")
        contents = encode_csv(rows)
        app = self.upload(contents, "gap_and_zero.csv")
        self.assertFalse(app.exception)
        for index, first in [(0, 200), (1, 10)]:
            values = self.chart_values(app, "y", 1, index)
            self.assertEqual(len(values), 3)
            self.assertEqual(values[0], first)
            self.assertTrue(values[1] is None or math.isnan(values[1]))
            self.assertEqual(values[2], 0)
        # Extend the selected window beyond the file; the requested boundary stays a gap.
        app.date_input[0].set_value(date(2026, 3, 31))
        with patch("streamlit.file_uploader", return_value=Upload(contents, "gap_and_zero.csv")):
            app.run()
        self.assertEqual(len(self.chart_values(app, "x", 1, 0)), 4)
        self.assertTrue(any("2 calendar dates have no selected records" in info.value for info in app.info))

    def test_time_series_missing_date_is_a_chart_gap_not_zero(self):
        from test_data_loader import encode_csv, sample_rows
        rows = sample_rows()
        rows[1]["date"] = "2026-04-03"
        contents = encode_csv(rows)
        app = self.upload(contents, "gap.csv")
        with patch("streamlit.file_uploader", return_value=Upload(contents, "gap.csv")):
            app.radio[1].set_value("Time Series").run()
        self.assertFalse(app.exception)
        periods = app.dataframe[0].value
        self.assertEqual(list(periods.recorded_days), [1, 0, 1])
        self.assertTrue(periods.spend.isna().iloc[1])
        values = self.chart_values(app, "y")
        import math
        self.assertTrue(math.isnan(values[1]) if values[1] is not None else True)
        self.assertEqual(values[0], 200)
        self.assertEqual(values[2], 100)
        spec = json.loads(app.get("plotly_chart")[0].proto.spec)
        self.assertFalse(spec["data"][0]["connectgaps"])
        self.assertTrue(any("1 selected calendar date has no records" in info.value for info in app.info))

    def test_time_series_missing_revenue_and_zero_denominators(self):
        from test_data_loader import encode_csv, sample_rows
        rows = sample_rows()
        rows[0]["revenue"] = ""
        rows[1]["spend"] = "0"
        contents = encode_csv(rows)
        app = self.upload(contents, "unknown.csv")
        with patch("streamlit.file_uploader", return_value=Upload(contents, "unknown.csv")):
            app.radio[1].set_value("Time Series").run()
            app.selectbox[1].set_value("ROAS").run()
            self.assertEqual(len(app.get("plotly_chart")), 0)
            self.assertTrue(app.dataframe[0].value.roas.isna().all())
            app.selectbox[1].set_value("Attributed revenue").run()
            self.assertEqual(app.dataframe[0].value.revenue.iloc[1], 0)
            self.assertEqual(self.chart_values(app, "y")[1], 0)
            app.selectbox[0].set_value("Weekly").run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.get("plotly_chart")), 0)
        self.assertEqual(app.dataframe[0].value.spend.iloc[0], 200)
        self.assertEqual(app.metric[1].value, "N/A")

    def test_time_series_negative_returns_and_single_day_marker(self):
        from test_data_loader import encode_csv, sample_rows
        contents = encode_csv(sample_rows())
        app = self.upload(contents, "returns.csv")
        with patch("streamlit.file_uploader", return_value=Upload(contents, "returns.csv")):
            app.radio[1].set_value("Time Series").run()
            app.selectbox[1].set_value("Ad-spend return").run()
            self.assertEqual(self.chart_values(app, "y"), [200, -100])
            app.date_input[0].set_value(date(2026, 4, 2)).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.dataframe[0].value), 1)
        self.assertEqual(self.chart_values(app, "y"), [-100])
        spec = json.loads(app.get("plotly_chart")[0].proto.spec)
        self.assertIn("markers", spec["data"][0]["mode"])
        self.assertEqual(spec["layout"]["yaxis"]["rangemode"], "tozero")


if __name__ == "__main__":
    unittest.main()
