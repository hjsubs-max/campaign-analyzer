"""Shared filters and aggregate metrics, reused by all dashboard views."""

import pandas as pd

COUNTS = ["impressions", "clicks", "conversions"]
SUMMARY_FIELDS = [*COUNTS, "spend", "revenue", "missing_revenue_rows", "ctr_pct",
                  "cvr_pct", "cpc", "cpa", "cpm", "roas", "ad_spend_return_pct",
                  "revenue_per_purchase"]


def filter_campaigns(data, start_date, end_date, channels, audiences, goals):
    """Intersect the four filters. Include both dates; an empty list selects none."""
    start, end = pd.Timestamp(start_date), pd.Timestamp(end_date)
    if pd.isna(start) or pd.isna(end):
        raise ValueError("Choose both a start date and an end date.")
    if start > end:
        raise ValueError("Start date must be on or before end date.")
    return data.loc[
        data.date.between(start, end)
        & data.channel.isin(channels)
        & data.audience.isin(audiences)
        & data.goal.isin(goals)
    ].copy()


def safe_ratio(numerator, denominator, multiplier=1):
    """None means unavailable; zero over a positive denominator is a valid zero."""
    if numerator is None or denominator is None or denominator == 0:
        return None
    return float(numerator / denominator) * multiplier


def summarize(data):
    """Sum raw measures first. Unknown revenue makes dependent metrics unavailable."""
    totals = {col: int(data[col].sum()) for col in COUNTS}
    spend = float(data.spend.sum())
    missing_revenue_rows = int(data.revenue.isna().sum())
    revenue = float(data.revenue.sum()) if len(data) and missing_revenue_rows == 0 else None
    return {
        **totals, "spend": spend, "revenue": revenue,
        "missing_revenue_rows": missing_revenue_rows,
        "ctr_pct": safe_ratio(totals["clicks"], totals["impressions"], 100),
        "cvr_pct": safe_ratio(totals["conversions"], totals["clicks"], 100),
        "cpc": safe_ratio(spend, totals["clicks"]),
        "cpa": safe_ratio(spend, totals["conversions"]),
        "cpm": safe_ratio(spend, totals["impressions"], 1000),
        "roas": safe_ratio(revenue, spend),
        "ad_spend_return_pct": safe_ratio(revenue - spend if revenue is not None else None, spend, 100),
        "revenue_per_purchase": safe_ratio(revenue, totals["conversions"]),
    }


def aggregate_campaigns(data, dimensions):
    """Apply the same metric definitions to channel/campaign/date groups."""
    if not dimensions:
        raise ValueError("Choose at least one grouping column.")
    rows = []
    grouper = dimensions[0] if len(dimensions) == 1 else dimensions
    for key, group in data.groupby(grouper, sort=True, dropna=False):
        key = (key,) if len(dimensions) == 1 else key
        rows.append({**dict(zip(dimensions, key)), **summarize(group)})
    return pd.DataFrame(rows, columns=[*dimensions, *SUMMARY_FIELDS])


def aggregate_time_series(data, start_date, end_date, frequency="Daily"):
    """Calendar periods, observed totals, and coverage; absent dates are not zeros.

    Weekly buckets run Monday–Sunday and are clipped to the selected dates.
    Coverage counts dates with at least one record, not campaign completeness.
    """
    start, end = pd.Timestamp(start_date), pd.Timestamp(end_date)
    if pd.isna(start) or pd.isna(end) or start > end:
        raise ValueError("Choose a valid start date on or before the end date.")
    start, end = start.normalize(), end.normalize()
    if frequency not in {"Daily", "Weekly"}:
        raise ValueError("Frequency must be Daily or Weekly.")
    selected = data.loc[data.date.between(start, end)].copy()
    calendar = pd.DataFrame({"date": pd.date_range(start, end, freq="D")})
    for frame in [selected, calendar]:
        frame["period"] = (frame.date.dt.to_period("W-SUN").dt.start_time
                           if frequency == "Weekly" else frame.date)
    coverage = calendar.groupby("period").agg(
        period_start=("date", "min"), period_end=("date", "max"), window_days=("date", "size"))
    grouped = aggregate_campaigns(selected, ["period"]).set_index("period")
    observations = selected.groupby("period").agg(
        recorded_days=("date", "nunique"), recorded_rows=("date", "size"))
    result = coverage.join(observations).join(grouped)
    for field in ["recorded_days", "recorded_rows"]:
        result[field] = result[field].fillna(0).astype(int)
    result["unrecorded_days"] = result.window_days - result.recorded_days
    result["partial_week"] = (result.window_days.lt(7) if frequency == "Weekly" else False)
    result["coverage"] = result.apply(
        lambda row: "No recorded data" if row.recorded_days == 0 else
        "Some dates have no records" if row.unrecorded_days else "All selected dates have records", axis=1)
    # Empty periods have NaN metrics after the join, even for spend/counts.
    return result.reset_index(drop=True)
