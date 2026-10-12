"""Read-only CSV inspection and reproducible controls for the next app milestone.

Run: uv run --locked python -B inspect_dataset.py
No CSV is modified. Output is saved to DATA_INSPECTION.json.
"""

import csv
import hashlib
import json
import math
from datetime import date
from decimal import Decimal
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "campaign_data_synthetic.csv"
COMPATIBLE = ROOT / "campaign_data_synthetic_compatible.csv"
COUNTS = ["impressions", "clicks", "conversions"]
MONEY = ["spend", "revenue"]
METADATA = ["campaign_name", "channel", "audience", "goal"]
EXPECTED = ["date", "campaign_id", *METADATA, *COUNTS, *MONEY, "currency", "dataset_type"]


def divide(numerator, denominator, multiplier=1):
    """Return None (JSON null / UI N/A) when a denominator is zero."""
    return float(numerator / denominator) * multiplier if denominator else None


def controls(rows):
    """Independent CSV + integer/Decimal calculation, without pandas aggregation."""
    totals = {col: sum(int(r[col]) for r in rows) for col in COUNTS}
    spend = sum((Decimal(r["spend"]) for r in rows), Decimal("0"))
    revenue = sum((Decimal(r["revenue"]) for r in rows), Decimal("0"))
    return {
        **totals, "spend": str(spend), "revenue": str(revenue),
        "ctr_pct": divide(totals["clicks"], totals["impressions"], 100),
        "cvr_pct": divide(totals["conversions"], totals["clicks"], 100),
        "cpc": divide(spend, totals["clicks"]),
        "cpa": divide(spend, totals["conversions"]),
        "cpm": divide(spend, totals["impressions"], 1000),
        "roas": divide(revenue, spend),
        "ad_spend_return_pct": divide(revenue - spend, spend, 100),
        "revenue_per_purchase": divide(revenue, totals["conversions"]),
    }


def run_inspection():
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        headers = reader.fieldnames
    assert headers == EXPECTED, "Unexpected source headers"
    raw = pd.DataFrame(rows)
    blank_cells = int(raw.isna().sum().sum() + raw.eq("").sum().sum())
    whitespace_cells = sum(int(raw[c].ne(raw[c].str.strip()).sum()) for c in raw)
    trimmed = raw.apply(lambda col: col.str.strip())
    dates = pd.to_datetime(trimmed["date"], format="%Y-%m-%d", errors="coerce")
    invalid_dates = int((dates.isna() | ~trimmed.date.str.fullmatch(r"\d{4}-\d{2}-\d{2}")).sum())
    numeric = trimmed[COUNTS + MONEY].apply(pd.to_numeric, errors="coerce")
    invalid_numbers = int(numeric.isna().sum().sum())
    nonfinite = sum(int((~numeric[c].map(math.isfinite)).sum()) for c in numeric)
    negatives = int(numeric.lt(0).sum().sum())
    fractions = int(numeric[COUNTS].mod(1).ne(0).sum().sum())
    checks = {
        "blank_or_null_cells": blank_cells,
        "cells_with_surrounding_whitespace": whitespace_cells,
        "exact_duplicate_rows": int(trimmed.duplicated().sum()),
        "duplicate_date_campaign_rows": int(trimmed.duplicated(["date", "campaign_id"], keep=False).sum()),
        "duplicate_date_campaign_channel_rows": int(trimmed.duplicated(["date", "campaign_id", "channel"], keep=False).sum()),
        "invalid_dates": invalid_dates, "invalid_numeric_cells": invalid_numbers,
        "nonfinite_numeric_cells": nonfinite, "negative_numeric_cells": negatives,
        "fractional_count_cells": fractions,
        "dates_after_check_date": int((dates > pd.Timestamp("2026-10-11")).sum()),
        "clicks_above_impressions_rows": int((numeric.clicks > numeric.impressions).sum()),
        "purchases_above_clicks_rows": int((numeric.conversions > numeric.clicks).sum()),
        "zero_purchases_with_nonzero_revenue_rows": int((numeric.conversions.eq(0) & numeric.revenue.ne(0)).sum()),
        "purchases_with_nonpositive_revenue_rows": int((numeric.conversions.gt(0) & numeric.revenue.le(0)).sum()),
        "campaigns_with_inconsistent_metadata": int(trimmed.groupby("campaign_id")[METADATA].nunique().gt(1).any(axis=1).sum()),
        "non_USD_rows": int(trimmed.currency.ne("USD").sum()),
        "rows_not_labelled_synthetic": int(trimmed.dataset_type.ne("synthetic").sum()),
    }
    assert all(value == 0 for value in checks.values()), checks
    df = trimmed.copy()
    df[COUNTS + MONEY] = numeric
    df["date"] = dates
    expected_days = pd.date_range(dates.min(), dates.max(), freq="D")
    missing_overall_days = len(expected_days.difference(dates.unique()))
    active_gaps = 0
    campaign_windows = []
    for campaign_id, group in df.groupby("campaign_id"):
        window = pd.date_range(group.date.min(), group.date.max(), freq="D")
        active_gaps += len(window.difference(group.date))
        first = group.iloc[0]
        campaign_windows.append({
            "campaign_id": campaign_id, "campaign_name": first.campaign_name,
            "channel": first.channel, "audience": first.audience, "goal": first.goal,
            "first_date": str(group.date.min().date()), "last_date": str(group.date.max().date()),
            "rows": len(group),
        })
    assert missing_overall_days == active_gaps == 0
    # Verify the supplied generator's documented active windows without regenerating data.
    for item in campaign_windows:
        name = item["campaign_name"]
        expected_start = "2026-05-15" if name.startswith("Summer Launch") else "2026-04-15" if name.startswith("Discover the Brand") else "2026-04-01"
        expected_end = "2026-08-31" if name.startswith("Summer Launch") else "2026-09-30"
        assert item["first_date"] == expected_start and item["last_date"] == expected_end
        assert item["rows"] == (date.fromisoformat(expected_end) - date.fromisoformat(expected_start)).days + 1
    totals = controls(rows)
    reference = {"impressions": 30156909, "clicks": 437337, "conversions": 7823, "spend": "306470.04", "revenue": "839690.13"}
    for key, expected in reference.items():
        assert totals[key] == expected, (key, totals[key], expected)
    for col in COUNTS:
        assert int(df[col].sum()) == totals[col]
    for col in MONEY:
        assert abs(Decimal(str(df[col].sum())) - Decimal(totals[col])) < Decimal("0.005")
    by_channel = {}
    for channel in sorted(df.channel.unique()):
        selected = [r for r in rows if r["channel"] == channel]
        by_channel[channel] = {"rows": len(selected), **controls(selected)}
    for col in COUNTS:
        assert sum(c[col] for c in by_channel.values()) == totals[col]
    for col in MONEY:
        assert sum((Decimal(c[col]) for c in by_channel.values()), Decimal("0")) == Decimal(totals[col])
    filtered_rows = [r for r in rows if "2026-06-01" <= r["date"] <= "2026-06-30" and r["channel"] == "Instagram" and r["audience"] == "Prospecting" and r["goal"] == "Sales"]
    pandas_filtered = df.loc[df.date.between("2026-06-01", "2026-06-30") & df.channel.eq("Instagram") & df.audience.eq("Prospecting") & df.goal.eq("Sales")]
    assert len(filtered_rows) == len(pandas_filtered) == 60
    assert pandas_filtered.campaign_id.nunique() == 2
    for col in COUNTS:
        assert int(pandas_filtered[col].sum()) == controls(filtered_rows)[col]
    for col in MONEY:
        assert abs(Decimal(str(pandas_filtered[col].sum())) - Decimal(controls(filtered_rows)[col])) < Decimal("0.005")
    edge_inputs = {
        ("2026-04-03", "CMP001"): [0, 0, 0, "0.00", "0.00"],
        ("2026-06-15", "CMP009"): [2050, 0, 0, "24.00", "0.00"],
        ("2026-05-09", "CMP014"): [1000, 14, 0, "7.80", "0.00"],
        ("2026-09-02", "CMP019"): [1000, 10, 2, "0.00", "190.00"],
    }
    edge_controls = []
    for (day, campaign_id), expected in edge_inputs.items():
        selected = [r for r in rows if r["date"] == day and r["campaign_id"] == campaign_id]
        assert len(selected) == 1
        actual = controls(selected)
        assert [actual[c] for c in COUNTS + MONEY] == expected
        edge_controls.append({"date": day, "campaign_id": campaign_id, **actual})
    assert edge_controls[0]["ctr_pct"] is None and edge_controls[0]["roas"] is None
    assert edge_controls[1]["ctr_pct"] == 0 and edge_controls[1]["cpc"] is None
    assert edge_controls[2]["cvr_pct"] == 0 and edge_controls[2]["cpa"] is None
    assert edge_controls[3]["cpc"] == 0 and edge_controls[3]["roas"] is None
    alias_map = {"goal": "campaign_goal", "dataset_type": "data_source"}
    with COMPATIBLE.open(newline="", encoding="utf-8-sig") as handle:
        compatible_rows = list(csv.DictReader(handle))
    compatible_matches = compatible_rows == [{alias_map.get(k, k): v for k, v in r.items()} for r in rows]
    assert compatible_matches
    boundary_rows = {day: sum(r["date"] == day for r in rows) for day in ["2026-04-01", "2026-09-30", "2026-10-01"]}
    assert boundary_rows == {"2026-04-01": 16, "2026-09-30": 20, "2026-10-01": 0}
    result = {
        "checked_on": "2026-10-11 (America/Los_Angeles)", "source": SOURCE.name,
        "source_sha256": source_hash, "dataset_type": "synthetic",
        "controlling_context": ["campaign_dataset_guide.txt", "campaign_dataset_generate_and_check.ipynb"],
        "grain": "one campaign on one reporting date; stable channel, audience, and goal per campaign",
        "unique_key": ["date", "campaign_id"], "rows": len(df), "columns": headers,
        "date_range": [str(dates.min().date()), str(dates.max().date())],
        "reporting_dates": int(dates.nunique()), "campaigns": int(df.campaign_id.nunique()),
        "channels": sorted(df.channel.unique()), "audiences": sorted(df.audience.unique()),
        "goals": sorted(df.goal.unique()), "currency": "USD", "checks": checks,
        "missing_overall_dates": missing_overall_days, "missing_dates_within_active_campaign_windows": active_gaps,
        "inactive_campaign_date_combinations": len(expected_days) * df.campaign_id.nunique() - len(df),
        "observed_rows_per_day_counts": {str(k): int(v) for k,v in df.groupby("date").size().value_counts().sort_index().items()},
        "zeros": {col: int(df[col].eq(0).sum()) for col in COUNTS + MONEY},
        "baseline": totals, "by_channel": by_channel, "campaign_active_windows": campaign_windows,
        "combined_filter_control": {"date_range": ["2026-06-01", "2026-06-30"], "channel": "Instagram", "audience": "Prospecting", "goal": "Sales", "rows": len(filtered_rows), "campaigns": 2, "metrics": controls(filtered_rows)},
        "boundary_rows": boundary_rows,
        "edge_case_controls": edge_controls, "compatible_copy_preserves_all_values": compatible_matches,
        "numeric_ranges": {c: {"min": float(df[c].min()), "median": float(df[c].median()), "max": float(df[c].max())} for c in COUNTS + MONEY},
        "assumptions_and_limits": [
            "All conversions are attributed purchases, including Traffic and Awareness goals.",
            "The supplied guide states purchases are assigned to one campaign in this simulation.",
            "Inactive dates are expected outside the documented campaign windows; do not invent missing records as zero activity.",
            "Synthetic channel factors and changes are chosen demonstration rules, not real advertising benchmarks or causal evidence.",
            "Revenue excludes taxes, shipping, refunds, product cost, agency fees, and operating costs.",
            "Ad-spend return is not full business profit ROI; CPA is cost per purchase event, not new-customer CAC.",
            "Unique people, reach, retention, and full profit cannot be inferred; the CSV has no user-level identifiers.",
            "Reporting dates have no timestamps or timezone conversion; production freshness is not assessable from this synthetic file.",
            "Clean default data does not exercise malformed dates, missing revenue, or duplicate-input error paths; those need separate fixtures later.",
        ],
    }
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == source_hash
    (ROOT / "DATA_INSPECTION.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(f"PASS: {len(df):,} synthetic rows, {df.campaign_id.nunique()} campaigns, {dates.nunique()} dates.")
    print("All structural checks passed; no missing days inside active windows.")
    print("Baseline:", json.dumps(totals, indent=2))
    print("Valid zero-value rows:", result["zeros"])
    print("Combined-filter reference:", json.dumps(result["combined_filter_control"], indent=2))
    print("Saved DATA_INSPECTION.json; both source CSVs remain unmodified.")
    return result


if __name__ == "__main__":
    run_inspection()
