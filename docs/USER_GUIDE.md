# Detailed app instructions and verification

These are optional instructions for using and checking the app. Start with
[README.md](../README.md) for the project summary, submission links, and quick start.
All commands below run from the folder containing `app.py`.

## Use and verify the app

1. Refresh the app at **http://127.0.0.1:8502**. If Streamlit shows **File change**,
   click **Rerun**. The default **Synthetic demo**
   should show “CSV validated: 4,040 rows loaded,” 24 campaigns, and the date
   window April 1–September 30, 2026.
2. In the sidebar, choose **Upload CSV**, then select `campaign_data_synthetic.csv`.
   You should see the same row count and a synthetic-data notice. The compatible
   copy also works; the original no longer needs manual header edits.
3. Use **Choose view** in the sidebar to switch between the four implemented views.
   The shared filters stay the same when changing views.
4. Use the sidebar's **Start date**, **End date**, **Channel**, **Audience**, and
   **Campaign goal** controls. Both dates are included, and all filters intersect.
   Cards, chart, table, and download use the same selected rows.
5. In Overview or Campaign Details, change **Preview rows** to control the bounded
   daily-record table, and use **Download
   filtered CSV** to export all selected records with normalized headers.
   Cards use every selected row, not just the displayed preview. **Reset filters**
   restores the full date range and all categories; new file contents get fresh defaults.
6. Try an invalid file or a duplicate campaign/day in a separate test copy.
   Expect an error and no stale preview. Missing revenue produces a warning and
   remains unknown; a genuine zero remains zero. Source CSVs are never overwritten.

The uploader accepts UTF-8 CSVs up to **10 MB / 100,000 rows**. The app's
**CSV format and validation** expander lists required fields and the row contract.

```sh
uv run --locked python -B -m unittest discover -s tests -v
```

Tests cover validation, both supplied header conventions, reference totals,
weighted rates, shared filters across views, reset, zero-value rows, missing revenue,
chart/card/table reconciliation, search, campaign selection, daily/weekly trends,
calendar gaps, partial weeks, and preview/error paths. Upload
branches use file-compatible bytes in AppTest. The real OS file picker was also
checked with the supplied original CSV. Actual daily Time Series and Overview
downloads reconcile to reference totals; grouped export payloads were checked
through AppTest. Chrome may ask before downloading several files quickly.

## Check the Overview numbers

With all filters reset, expect **4,040 selected rows** and these six cards:
USD **306,470.04 spend**, USD **839,690.13 attributed revenue**, **7,823 purchases**,
**1.45% CTR**, USD **39.18 CPA**, and **2.74× ROAS**. More metrics and formulas
appear under **Metric details and definitions**.

Below the channel chart, **Spend and conversions over time** shows daily spend
and purchases in two aligned panels with the same dates and separate labelled
units. Each panel uses summed daily inputs from all selected rows, not the table
preview. With filters reset, each panel has 183 dates; their values total USD
306,470.04 spend and 7,823 purchases. A date with no records remains a gap, even
when the selected window extends beyond the file. Recorded zeros stay zero.
Both panels have a zero baseline. The patterns alone do not establish causal lift.

For a combined-filter check, set dates to **June 1–30, 2026**, Channel to
**Instagram**, Audience to **Prospecting**, and Campaign goal to **Sales**.
Expect **60 selected rows**, **2 campaigns**, USD **9,394.52 spend**, USD
**20,205.07 revenue**, **175 purchases**, **1.46% CTR**, USD **53.68 CPA**, and
**2.15× ROAS**. Choose Preview rows **100** to see all 60 records. Sum the
downloaded spend column and compare it with both the card and chart.

Clear Channel to check the no-data message. No stale cards, chart, or table should
remain. Reversing the dates produces a readable error. Reset restores results.

For a zero-spend check, choose **September 2, 2026** for both dates, **Twitter**,
**Prospecting**, and **Sales**. The credit-funded row has USD **0.00 spend**,
USD **190.00 revenue**, **2 purchases**, USD **0.00 CPA**, and **N/A ROAS**.
Zero divided by a positive denominator is zero; a zero denominator is unavailable.

If selected rows contain unknown revenue, Revenue, ROAS, ad-spend return, and
revenue per purchase display **N/A** with a warning. Spend and count-based metrics
still work. Filtering out those unknown records can restore complete revenue.

## Use Platform Comparison

Select **Platform Comparison** in the sidebar. Its cards summarize all rows allowed
by the global filters. **Compare metric** changes the channel chart; the table
shows volume, spend, revenue, and rates calculated from each channel's totals.
For complete inputs, the channel table's additive measures reconcile with Overview
for the same filters. Do not add known revenue cells to invent a complete revenue
total when any channel's revenue is unknown.
Rates themselves should not be added or averaged to obtain overall rates.

With all filters reset, expect four channel rows. Selecting **ROAS** shows
approximately **2.67× Facebook**, **3.02× Instagram**, **3.03× Pinterest**, and
**1.96× Twitter**. These are synthetic examples, not real channel benchmarks.
The comparison selector also supports Spend, Attributed revenue, Purchases, CTR,
Purchase conversion rate, CPC, CPA, CPM, and Ad-spend return.

Missing/undefined metric values remain blank (N/A) in the table. If a channel's
chosen metric is unavailable, it is omitted from that chart with an explanation;
no daily records are discarded or values replaced with zero. If every channel's
metric is unavailable, choose another metric. Negative ad-spend returns keep
their signs and a visible zero baseline. **Download channel comparison** exports
the grouped results for the current shared filters.

## Use searchable Campaign Details

Select **Campaign Details**. **Search campaigns** searches ID, name, channel,
audience, and goal, ignoring case and treating punctuation as literal text.
The searchable table has one aggregated row per matching campaign. The
**Campaign** selector then shows one campaign's cards and daily records.
Both search and selection work within the global filters; they cannot restore
campaigns excluded by date, channel, audience, or goal.

Try these checks with global filters reset:

- Search `summer launch`: expect four matching campaigns.
- Search `CMP010`: expect one matching campaign, **Summer Launch - Instagram**,
  and **109 daily records** from May 15–August 31, 2026. Its cards should show
  USD **20,971.68 spend**, USD **60,626.37 revenue**, and **500 purchases**.
- Search `[`: expect a clear no-match message, not a regular-expression error.
  Clear the search to restore the full campaign list.

For the June + Instagram + Prospecting + Sales control, the campaign summary has
two rows: **CMP007** and **CMP010**. Their totals reconcile with Overview's
USD 9,394.52 spend, USD 20,205.07 revenue, and 175 purchases. Selecting CMP010
shows its **30 June records**; cards now describe only that selected campaign.

**Download matching campaigns** exports the searched aggregate table. **Download
filtered CSV** under the daily records exports the selected campaign's records.
Reset restores the global filters; clear campaign search separately. Search and
campaign selection affect Campaign Details only.

## Use Time Series

Select **Time Series**. The six cards describe all rows within the shared filters.
Choose **Daily** or **Weekly** under **Time interval**, then choose **Trend metric**.
The chart has one point per period and the table shows totals plus date coverage.
Weekly periods run Monday–Sunday; the first and last periods are clipped to the
chosen dates and labelled **Partial week** when fewer than seven days are selected.
Ratios use each period's summed inputs. Never average daily ROAS or CTR to obtain
a weekly result, or average weekly rates to obtain the overall rate.

With filters reset, expect **183 daily periods** or **27 weekly periods**. Both
tables reconcile to USD **306,470.04 spend**, USD **839,690.13 revenue**, and
**7,823 purchases**. The first weekly row covers **April 1–5** (five days); the
last covers **September 28–30** (three days). They are smaller date windows,
so their totals should not be compared as if they were full seven-day weeks.

Try June 1–30 + Instagram + Prospecting + Sales: expect **30 daily periods**,
**60 campaign-day records**, and USD **9,394.52 spend**. Weekly mode gives five
periods, with June 29–30 labelled partial. Change the metric to ROAS: each point
must equal that period's revenue divided by that period's spend.

Dates with no selected records stay in the table as **No recorded data** with
blank metrics and a line gap. A recorded zero remains zero. Weeks with some dates
without records show observed totals and explicit coverage; no activity is invented
for those dates. **Days with records** means at least one selected campaign
reported, not proof that every campaign reported. Missing revenue makes only that
period's revenue-dependent metrics N/A; the overall revenue card remains N/A if
any selected revenue is unknown. Zero denominators also produce N/A and gaps.

**Download time series** exports the selected interval's full period table,
including coverage and unavailable values. It exports aggregated results, not the
daily campaign records. Trend controls affect Time Series only.

See `PROJECT_BRIEF.md` for the requirements and `PROGRESS.md` for actual setup
actions and check results. No source changes or commits were made in the course repo.

## Reproduce the dataset inspection

```sh
uv run --locked python -B inspect_dataset.py
```

The script reads both CSVs, performs checks, and writes `DATA_INSPECTION.json`;
it does not modify the source data. `dataset_inspection.ipynb` contains a readable
companion with executed Python-cell outputs. It was checked without a Jupyter
kernel because notebook packages are not installed in this minimal environment.

The original `campaign_data_synthetic.csv` is our working demo source. Its 4,040
rows represent 24 campaigns over 183 dates. All conversions are attributed
purchases, all money is USD, and the data is synthetic. The compatible copy differs
only in the headers `goal`/`campaign_goal` and `dataset_type`/`data_source`.
The uploader accepts these explicit mappings and keeps `goal` and `dataset_type`
as its internal and exported names. Ambiguous files containing both names for
one field are rejected so there is no silent choice between conflicting columns.

Default-data controls: USD **306,470.04 spend**, USD **839,690.13 revenue**,
**7,823 purchases**, **1.450205% CTR**, and **2.739877× ROAS**. Missing revenue
must not be treated as zero, and zero denominators must display N/A.

`data_loader.py` holds input validation. `analysis.py` holds shared filters and
metrics calculated from totals. `app.py` loads data, applies filters, and selects
the view. `views.py` renders all four views using common cards, charts, and tables.
Additional columns are retained. Provenance labels are
preserved; a file without a label is marked unspecified rather than assumed real.

## Chart design notes

Question: how much advertising spend belongs to each channel within the current
selection? Plotly horizontal bars show one summed spend per channel, sorted by
spend. The full demo has four channels; filters may legitimately leave fewer.
The quantitative axis starts at zero, the palette is a single blue (#357ABD),
and category labels provide identity without a redundant legend. Exact amounts
appear on bars; hover includes impressions, clicks, purchases, attributed revenue,
and unknown-revenue counts. The caption gives currency, dates, audiences, and goals.
The chart fills the Streamlit container at 340 px height. Platform Comparison uses
the same horizontal-bar design for its selected metric, with appropriate units
and signed axes for negative returns. Hover retains denominator/volume context.
Campaign Details uses tables for lookup and daily inspection rather than adding
an unrelated chart. Desktop chart/table rendering, navigation, and campaign search
were inspected in the live browser. A 900-pixel Chrome responsive preview exposed
truncated card values; metric rows now wrap below 1,100 pixels and show complete
values. All four views remain reachable in that preview. This was browser emulation,
not a physical-phone test. Wide tables use horizontal scrolling.
Time Series uses a blue line with point markers, chronological dates, explicit
metric units, a visible zero baseline, and `connectgaps=False`. Hover includes
period boundaries, date coverage, record count, and the formatted metric value.
Markers keep a single recorded day visible. Missing dates and undefined ratios
stay gaps; the table preserves all periods. Weekly points summarize the observed
records in each labelled window, including partial weeks.

