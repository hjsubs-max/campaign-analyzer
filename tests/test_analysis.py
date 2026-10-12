import json
import unittest
from pathlib import Path

import pandas as pd

from analysis import aggregate_campaigns, aggregate_time_series, filter_campaigns, safe_ratio, summarize
from data_loader import load_campaign_csv
from test_data_loader import encode_csv, sample_rows

ROOT = Path(__file__).resolve().parents[1]


class AnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_campaign_csv((ROOT / "campaign_data_synthetic.csv").read_bytes()).data
        cls.controls = json.loads((ROOT / "DATA_INSPECTION.json").read_text())

    def assert_controls(self, actual, expected):
        for key, value in expected.items():
            with self.subTest(metric=key):
                if value is None:
                    self.assertIsNone(actual[key])
                else:
                    self.assertAlmostEqual(actual[key], float(value), places=7)

    def test_baseline_matches_independent_dataset_controls(self):
        self.assert_controls(summarize(self.data), self.controls["baseline"])

    def test_rates_use_aggregate_numerators_and_denominators(self):
        rows = sample_rows()
        rows[1]["impressions"] = "100"  # CTRs are 10% and 50%; averaging gives a wrong 30%.
        metrics = summarize(load_campaign_csv(encode_csv(rows)).data)
        self.assertAlmostEqual(metrics["ctr_pct"], 150 / 1100 * 100)
        self.assertNotEqual(metrics["ctr_pct"], 30)
        self.assertEqual(metrics["cpa"], 30)
        self.assertEqual(metrics["roas"], 2)

    def test_combined_filter_and_inclusive_dates(self):
        selected = filter_campaigns(self.data, "2026-06-01", "2026-06-30", ["Instagram"], ["Prospecting"], ["Sales"])
        control = self.controls["combined_filter_control"]
        self.assertEqual(len(selected), control["rows"])
        self.assertEqual(selected.campaign_id.nunique(), control["campaigns"])
        self.assert_controls(summarize(selected), control["metrics"])
        self.assertEqual(selected.date.min().strftime("%Y-%m-%d"), "2026-06-01")
        self.assertEqual(selected.date.max().strftime("%Y-%m-%d"), "2026-06-30")

    def test_empty_categories_outside_dates_and_reversed_dates(self):
        for channels, audiences, goals in [([], ["Prospecting"], ["Sales"]), (["Instagram"], [], ["Sales"]), (["Instagram"], ["Prospecting"], [])]:
            with self.subTest(channels=channels, audiences=audiences, goals=goals):
                self.assertTrue(filter_campaigns(self.data, "2026-04-01", "2026-09-30", channels, audiences, goals).empty)
        self.assertTrue(filter_campaigns(self.data, "2026-10-01", "2026-10-31", ["Instagram"], ["Prospecting"], ["Sales"]).empty)
        with self.assertRaisesRegex(ValueError, "Start date"):
            filter_campaigns(self.data, "2026-09-30", "2026-04-01", [], [], [])

    def test_documented_zero_denominator_cases(self):
        for control in self.controls["edge_case_controls"]:
            with self.subTest(day=control["date"], campaign=control["campaign_id"]):
                selected = self.data.loc[self.data.date.eq(control["date"]) & self.data.campaign_id.eq(control["campaign_id"])]
                expected = {k: v for k, v in control.items() if k not in {"date", "campaign_id"}}
                self.assert_controls(summarize(selected), expected)
        self.assertIsNone(safe_ratio(0, 0))
        self.assertEqual(safe_ratio(0, 100), 0)

    def test_missing_revenue_blocks_only_dependent_metrics(self):
        rows = sample_rows()
        rows[0]["revenue"] = ""
        data = load_campaign_csv(encode_csv(rows)).data
        metrics = summarize(data)
        for key in ["revenue", "roas", "ad_spend_return_pct", "revenue_per_purchase"]:
            self.assertIsNone(metrics[key])
        self.assertEqual(metrics["missing_revenue_rows"], 1)
        self.assertEqual(metrics["spend"], 300)
        self.assertEqual(metrics["cpa"], 30)
        # Excluding the unknown record restores known-zero revenue and ROAS.
        selected = filter_campaigns(data, "2026-04-01", "2026-04-02", ["Instagram"], ["Retargeting"], ["Traffic"])
        known = summarize(selected)
        self.assertEqual(known["revenue"], 0)
        self.assertEqual(known["roas"], 0)
        grouped = aggregate_campaigns(data, ["channel"])
        self.assertTrue(grouped.loc[grouped.channel.eq("Facebook"), "revenue"].isna().all())
        self.assertEqual(grouped.loc[grouped.channel.eq("Instagram"), "revenue"].iloc[0], 0)

    def test_grouped_totals_reconcile_and_empty_grouping_is_safe(self):
        for dimensions in [["channel"], ["campaign_id"], ["date"], ["channel", "goal"]]:
            grouped = aggregate_campaigns(self.data, dimensions)
            for col in ["impressions", "clicks", "conversions", "spend", "revenue"]:
                self.assertAlmostEqual(grouped[col].sum(), self.data[col].sum(), places=6)
        empty = self.data.iloc[:0]
        self.assertTrue(aggregate_campaigns(empty, ["channel"]).empty)
        self.assertIsNone(summarize(empty)["revenue"])

    def test_time_periods_reconcile_with_source_totals(self):
        for frequency, count in [("Daily", 183), ("Weekly", 27)]:
            periods = aggregate_time_series(self.data, "2026-04-01", "2026-09-30", frequency)
            self.assertEqual(len(periods), count)
            self.assertEqual(periods.recorded_days.sum(), 183)
            self.assertEqual(periods.recorded_rows.sum(), 4040)
            self.assertEqual(periods.unrecorded_days.sum(), 0)
            for field in ["impressions", "clicks", "conversions", "spend", "revenue"]:
                self.assertAlmostEqual(periods[field].sum(), float(self.controls["baseline"][field]), places=6)
            if frequency == "Weekly":
                self.assertEqual(list(periods.window_days.iloc[[0, -1]]), [5, 3])
                self.assertEqual(periods.partial_week.sum(), 2)

    def test_weekly_weighted_rates_and_clipped_monday_boundaries(self):
        rows = sample_rows()
        rows[1]["impressions"] = "100"
        data = load_campaign_csv(encode_csv(rows)).data
        periods = aggregate_time_series(data, "2026-04-01", "2026-04-06", "Weekly")
        first = periods.iloc[0]
        self.assertAlmostEqual(first.ctr_pct, 150 / 1100 * 100)
        self.assertEqual(first.roas, 2)
        self.assertEqual(first.recorded_days, 2)
        self.assertEqual(first.unrecorded_days, 3)
        self.assertEqual(first.window_days, 5)
        self.assertEqual(first.period_start, pd.Timestamp("2026-04-01"))
        self.assertEqual(first.period_end, pd.Timestamp("2026-04-05"))
        self.assertEqual(periods.iloc[1].period_start, pd.Timestamp("2026-04-06"))
        self.assertTrue(pd.isna(periods.iloc[1].spend))

    def test_absent_dates_are_unknown_but_recorded_zeros_stay_zero(self):
        row = sample_rows()[0]
        row.update(impressions="0", clicks="0", conversions="0", spend="0", revenue="0")
        data = load_campaign_csv(encode_csv([row])).data
        periods = aggregate_time_series(data, "2026-03-31", "2026-04-02")
        self.assertEqual(list(periods.recorded_days), [0, 1, 0])
        self.assertEqual(list(periods.coverage), ["No recorded data", "All selected dates have records", "No recorded data"])
        self.assertEqual(periods.spend.iloc[1], 0)
        self.assertEqual(periods.revenue.iloc[1], 0)
        self.assertTrue(periods.loc[[0, 2], ["spend", "impressions", "revenue"]].isna().all().all())
        self.assertTrue(periods.roas.isna().all())
        self.assertTrue(aggregate_time_series(data.iloc[:0], "2026-04-01", "2026-04-02").spend.isna().all())

    def test_unknown_revenue_is_scoped_to_period_and_week(self):
        rows = sample_rows()
        rows[0]["revenue"] = ""
        data = load_campaign_csv(encode_csv(rows)).data
        daily = aggregate_time_series(data, "2026-04-01", "2026-04-02")
        self.assertTrue(pd.isna(daily.revenue.iloc[0]))
        self.assertEqual(daily.roas.iloc[1], 0)
        weekly = aggregate_time_series(data, "2026-04-01", "2026-04-02", "Weekly").iloc[0]
        self.assertEqual(weekly.missing_revenue_rows, 1)
        self.assertTrue(pd.isna(weekly.revenue))
        self.assertTrue(pd.isna(weekly.roas))
        self.assertEqual(weekly.spend, 300)

    def test_time_series_respects_window_and_rejects_invalid_arguments(self):
        data = load_campaign_csv(encode_csv(sample_rows())).data
        period = aggregate_time_series(data, "2026-04-02", "2026-04-02").iloc[0]
        self.assertEqual(period.recorded_rows, 1)
        self.assertEqual(period.spend, 100)
        for start, end, frequency in [("2026-04-02", "2026-04-01", "Daily"),
                                      (None, "2026-04-01", "Daily"),
                                      ("2026-04-01", "2026-04-02", "Monthly")]:
            with self.assertRaises(ValueError):
                aggregate_time_series(data, start, end, frequency)


if __name__ == "__main__":
    unittest.main()
