"""Validate daily campaign CSVs without dropping records or inventing revenue."""

import csv
import math
from dataclasses import dataclass
from io import StringIO

import pandas as pd

MAX_UPLOAD_MB = 10
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
MAX_ROWS = 100_000
ALIASES = {"campaign_goal": "goal", "data_source": "dataset_type"}
DIMENSIONS = ["campaign_id", "campaign_name", "channel", "audience", "goal"]
COUNTS = ["impressions", "clicks", "conversions"]
REQUIRED = ["date", *DIMENSIONS, *COUNTS, "spend", "currency"]
MISSING_REVENUE = {"", "na", "n/a", "nan", "null", "none"}


class CSVValidationError(ValueError):
    """An input error suitable for showing directly to the uploader's user."""


@dataclass
class LoadedCSV:
    data: pd.DataFrame
    warnings: list[str]
    mapped_headers: list[str]


def _row_examples(mask):
    # Header occupies CSV row 1; examples refer to logical records, not lines in quoted cells.
    return ", ".join(str(int(i) + 2) for i in mask[mask].index[:3])


def load_campaign_csv(contents: bytes) -> LoadedCSV:
    if len(contents) > MAX_UPLOAD_BYTES:
        raise CSVValidationError(f"CSV is too large. The limit is {MAX_UPLOAD_MB} MB.")
    try:
        text = contents.decode("utf-8-sig")
        reader = csv.reader(StringIO(text, newline=""), strict=True)
        original_headers = next(reader)
        headers = [name.strip().lower() for name in original_headers]
        if not headers or any(not name for name in headers):
            raise CSVValidationError("Use a CSV with a non-empty header row and named columns.")
        if len(headers) != len(set(headers)):
            raise CSVValidationError("Duplicate column names found. Each column needs a unique name.")
        canonical = [ALIASES.get(name, name) for name in headers]
        if len(canonical) != len(set(canonical)):
            raise CSVValidationError("Use either goal or campaign_goal, and either dataset_type or data_source; keep one column for each.")
        missing = sorted(set(REQUIRED) - set(canonical))
        if missing:
            raise CSVValidationError("Missing required columns: " + ", ".join(missing))
        records = []
        for record_number, record in enumerate(reader, start=2):
            if len(record) != len(headers):
                raise CSVValidationError(f"CSV record {record_number} has {len(record)} fields; expected {len(headers)}. Check commas, quoting, or blank lines.")
            records.append(record)
            if len(records) > MAX_ROWS:
                raise CSVValidationError(f"CSV contains too many records. The limit is {MAX_ROWS:,} rows.")
    except (UnicodeDecodeError, StopIteration) as exc:
        raise CSVValidationError("Use a non-empty UTF-8 CSV with a header and data rows.") from exc
    except csv.Error as exc:
        raise CSVValidationError("Could not parse the CSV. Check its quotation marks and separators.") from exc
    if not records:
        raise CSVValidationError("The CSV has a header but no data rows.")
    df = pd.DataFrame(records, columns=canonical, dtype=str).apply(lambda col: col.str.strip())
    blank = df[REQUIRED].eq("").sum()
    if blank.any():
        details = ", ".join(f"{col}: {int(count)}" for col, count in blank.items() if count)
        raise CSVValidationError("Blank required cells (counts): " + details)
    dates = pd.to_datetime(df.date, format="%Y-%m-%d", errors="coerce")
    bad_dates = dates.isna() | ~df.date.str.fullmatch(r"\d{4}-\d{2}-\d{2}")
    if bad_dates.any():
        raise CSVValidationError(f"Invalid dates in CSV records {_row_examples(bad_dates)}. Use YYYY-MM-DD.")
    df["date"] = dates
    for col in COUNTS + ["spend"]:
        values = pd.to_numeric(df[col], errors="coerce")
        invalid = values.isna() | ~values.map(math.isfinite) | values.lt(0)
        if invalid.any():
            raise CSVValidationError(f"{col} must contain finite, non-negative numbers. Check CSV records {_row_examples(invalid)}.")
        if col in COUNTS:
            invalid = values.mod(1).ne(0) | values.gt(2**53 - 1)
            if invalid.any():
                raise CSVValidationError(f"{col} must contain whole-number counts within the supported range. Check CSV records {_row_examples(invalid)}.")
            df[col] = values.astype("int64")
            if sum(int(value) for value in df[col]) > 2**53 - 1:
                raise CSVValidationError(f"Total {col} exceeds the supported exact-count range.")
        else:
            df[col] = values.astype(float)
            if not math.isfinite(float(df[col].sum())):
                raise CSVValidationError("Total spend is outside the supported numeric range.")
    if df.clicks.gt(df.impressions).any():
        raise CSVValidationError("Clicks exceed impressions. This app expects a click-based campaign funnel.")
    if df.conversions.gt(df.clicks).any():
        raise CSVValidationError("Conversions exceed clicks. This app expects at most one attributed conversion per click.")
    df["currency"] = df.currency.str.upper()
    if not df.currency.str.fullmatch(r"[A-Z]{3}").all():
        raise CSVValidationError("Currency must be a three-letter code such as USD.")
    if df.currency.nunique() != 1:
        raise CSVValidationError("Multiple currencies cannot be added together. Convert the file to one currency first.")
    duplicate = df.duplicated(["date", "campaign_id"], keep=False)
    if duplicate.any():
        raise CSVValidationError(f"{int(duplicate.sum())} records share the same date and campaign_id. Supply one row per campaign per day.")
    if df.groupby("campaign_id")[["campaign_name", "channel", "audience", "goal"]].nunique().gt(1).any().any():
        raise CSVValidationError("A campaign_id has inconsistent name, channel, audience, or goal. Use stable campaign IDs.")
    warnings = []
    if "revenue" not in df:
        df["revenue"] = float("nan")
        missing_revenue = pd.Series(True, index=df.index)
    else:
        missing_revenue = df.revenue.str.casefold().isin(MISSING_REVENUE)
        values = pd.to_numeric(df.revenue, errors="coerce")
        invalid = ~missing_revenue & (values.isna() | ~values.map(math.isfinite) | values.lt(0))
        if invalid.any():
            raise CSVValidationError(f"Revenue must be non-negative numbers or missing values. Check CSV records {_row_examples(invalid)}.")
        df["revenue"] = values.where(~missing_revenue, float("nan")).astype(float)
        if not math.isfinite(float(df.revenue.sum())):
            raise CSVValidationError("Known revenue exceeds the supported numeric range.")
    if missing_revenue.any():
        warnings.append(f"Revenue is missing in {int(missing_revenue.sum()):,} of {len(df):,} rows. It remains unknown, not zero; revenue-based metrics require complete revenue for the selected rows.")
    if "dataset_type" not in df:
        df["dataset_type"] = "unspecified"
    else:
        df["dataset_type"] = df.dataset_type.str.lower().replace("", "unspecified")
    normalized_headers = [f"{old} → {new}" for old, new in zip(headers, canonical) if old != new]
    return LoadedCSV(df.sort_values(["date", "campaign_id"]).reset_index(drop=True), warnings, normalized_headers)
