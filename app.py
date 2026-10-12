"""One data source and filter pipeline for all four campaign views."""

from importlib.metadata import version
from pathlib import Path
import hashlib

import streamlit as st

from analysis import filter_campaigns
from data_loader import CSVValidationError, MAX_UPLOAD_MB, load_campaign_csv
from views import render_campaign_details, render_overview, render_platform_comparison, render_time_series

st.set_page_config(page_title="Ad Campaign Performance Analyzer", page_icon="📊", layout="wide")

# Keep complete metric values readable when the sidebar reduces available space.
st.html("""<style>
@media (max-width: 1100px) {
  [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) {
    flex-wrap: wrap;
  }
  [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"] {
    flex: 1 1 220px;
    min-width: min(220px, 100%);
  }
  [data-testid="stMetricValue"] { font-size: 1.75rem; }
}
</style>""")


@st.cache_data(show_spinner=False)
def read_data(contents):
    return load_campaign_csv(contents)


def reset_filters(keys, defaults):
    for name, key in keys.items():
        st.session_state[key] = defaults[name]


st.title("Ad Campaign Performance Analyzer")
st.caption("Hassan · Maven Week 1 · Path B")

with st.sidebar:
    st.header("Campaign data")
    source = st.radio("Data source", ["Synthetic demo", "Upload CSV"], key="data_source")
    uploaded = None
    if source == "Upload CSV":
        uploaded = st.file_uploader("Upload campaign CSV", type=["csv"], max_upload_size=MAX_UPLOAD_MB,
            help="UTF-8 CSV, up to 10 MB. Original and compatible headers are supported.", key="campaign_csv")
    st.header("View")
    view = st.radio("Choose view", ["Overview", "Platform Comparison", "Campaign Details", "Time Series"], key="view")

with st.expander("CSV format and validation"):
    st.markdown("""
    **Required columns:** `date`, `campaign_id`, `campaign_name`, `channel`,
    `audience`, `goal`, `impressions`, `clicks`, `conversions`, `spend`, `currency`.

    `campaign_goal` is accepted as an alias for `goal`. `data_source` is accepted
    as an alias for the optional `dataset_type` label. Keep only one header for
    each field. Column names ignore capitalization and surrounding whitespace.

    Supply **one campaign per day**, with a stable name, channel, audience, and
    goal. Dates use YYYY-MM-DD. Counts are non-negative integers; conversions
    must not exceed clicks, and clicks must not exceed impressions. Money must
    be finite, non-negative, and use one currency. Extra columns are retained.

    `revenue` is optional. Blank revenue stays unknown and produces a warning;
    it is never replaced with zero. Required missing values and invalid or
    duplicate records are rejected with an explanation. No rows are dropped.
    The limit is 10 MB and 100,000 rows.
    """)

if source == "Upload CSV" and uploaded is None:
    st.info("Choose a campaign CSV in the sidebar to validate it and see a preview.")
    st.stop()

try:
    if source == "Synthetic demo":
        path = Path(__file__).parent / "campaign_data_synthetic.csv"
        contents, source_name = path.read_bytes(), path.name
    else:
        contents, source_name = uploaded.getvalue(), uploaded.name
    loaded = read_data(contents)
except CSVValidationError as exc:
    st.error(str(exc))
    st.info("Correct the CSV and upload it again. No rows were silently discarded.")
    st.stop()
except OSError:
    st.error("The demonstration CSV could not be opened. Choose Upload CSV to supply your dataset.")
    st.stop()

data = loaded.data
if source == "Synthetic demo" or data.dataset_type.eq("synthetic").any():
    st.warning("Synthetic demonstration data is included. These figures are invented and are not real advertising results.")
else:
    st.info("Uploaded data: structure is validated. Verify its provenance and attribution before using it for decisions.")
if loaded.warnings:
    with st.expander("File-level warnings"):
        for warning in loaded.warnings:
            st.caption(warning)
if loaded.mapped_headers:
    st.caption("Mapped headers: " + "; ".join(loaded.mapped_headers))

st.success(f"CSV validated: {len(data):,} rows loaded.")
st.caption(f"Source: {source_name} · {data.campaign_id.nunique()} campaigns · "
    f"{data.date.min():%b %d, %Y} – {data.date.max():%b %d, %Y} · Currency: {data.currency.iloc[0]}")

currency = data.currency.iloc[0]
prefix = hashlib.sha256(contents).hexdigest()[:12]
defaults = {
    "start": data.date.min().date(), "end": data.date.max().date(),
    "channels": sorted(data.channel.unique()), "audiences": sorted(data.audience.unique()),
    "goals": sorted(data.goal.unique()),
}
keys = {name: f"filters_{prefix}_{name}" for name in defaults}
for name, key in keys.items():
    if key not in st.session_state:
        st.session_state[key] = defaults[name]
with st.sidebar:
    st.header("Shared filters")
    # Session state supplies values; separate widget defaults would conflict on reset.
    start = st.date_input("Start date", key=keys["start"])
    end = st.date_input("End date", key=keys["end"])
    channels = st.multiselect("Channel", defaults["channels"], key=keys["channels"])
    audiences = st.multiselect("Audience", defaults["audiences"], key=keys["audiences"])
    goals = st.multiselect("Campaign goal", defaults["goals"], key=keys["goals"])
    st.button("Reset filters", on_click=reset_filters, args=(keys, defaults))
    st.caption("Both dates are included. Clearing a category selects no rows. New file contents get fresh filter defaults.")

try:
    # Every view receives this single filtered frame.
    filtered = filter_campaigns(data, start, end, channels, audiences, goals)
except ValueError as exc:
    st.error(str(exc))
    st.stop()

st.header(view)
st.caption(f"{start:%b %d, %Y} – {end:%b %d, %Y} · {len(filtered):,} selected rows · {filtered.campaign_id.nunique()} campaigns")
if filtered.empty:
    st.info("No rows match these filters. Widen the dates or select additional categories.")
    st.stop()

context = f"{start:%b %d} – {end:%b %d, %Y} · Audiences: {', '.join(audiences)} · Goals: {', '.join(goals)}"
if view == "Overview":
    render_overview(filtered, currency, context, start, end)
elif view == "Platform Comparison":
    render_platform_comparison(filtered, currency, context)
elif view == "Campaign Details":
    render_campaign_details(filtered, currency, prefix)
else:
    render_time_series(filtered, currency, context, start, end)

st.subheader("Ready for your walkthrough")
st.write("All four views are built. Use SUBMISSION_GUIDE.md to rehearse your course demo and capture screenshots.")

with st.expander("Installed packages"):
    for package in ["streamlit", "pandas", "plotly"]:
        st.write(f"{package}: {version(package)}")
