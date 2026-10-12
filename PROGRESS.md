# Progress — Hassan's Week 1 Path B project

Date: **October 11, 2026 (America/Los_Angeles)**.

## Milestone 1: isolated setup

Status: **Complete.** The isolated environment and initial page were verified.

**Current project:** `campaign-analyzer`, at **http://127.0.0.1:8502**.

**Latest milestone:** All four views, including daily/weekly Time Series, are
complete, using shared filters. The original supplied CSV is the default
synthetic demo source. Browser checks and the submission guide are complete;
Official submission requirements are verified and the Overview paired trend is
complete. The private Google Doc is in Hassan's W1 Project folder with six genuine
screenshots and his expanded reflection. The same Doc now has a Start here page,
three main narrative pages and six labelled evidence appendices. A concise README
links to optional detailed usage; reviewer navigation and layout were verified.
Hassan supplied his recording and chose the Loom link; it is linked from Doc
page 1 and README. Duration, contents, and public viewing access are unverified.
At Hassan's request, proceed one step at a time: GitHub publication, final
duration/access checks, and form submission.
The local address remains
**http://127.0.0.1:8502**.

### Workspace and tool checks

- Workspace root: `Project`. It is not itself a Git repository.
- Course repo: `Mastering-Agentic-AI-Week1`; Git recognizes it as a repository.
  Existing unrelated work was left intact. Secret file contents were not read.
- Default `python3`: `/usr/bin/python3`, Python **3.9.6**.
- Installed uv-managed Python: **3.11.15**, used for this starter.
- uv: **0.13.0**, at `/Users/hassanjaved/.local/bin/uv`.
- Git: **2.54.0 (Apple Git-157)**, at `/usr/bin/git`.
- Created `campaign-analyzer` alongside the course repository, with its own
  environment and no selected dataset at the setup milestone.

### Actual changes

- Added `pyproject.toml` with pandas, Plotly, Streamlit, and Python >=3.11.
- Added `.python-version` to select Python 3.11 and `.gitignore` for local
  environment, caches, and secrets.
- Added a minimal `app.py`: title, working-starter notice, no-dataset notice,
  planned view descriptions, and installed package versions.
- Added `PROJECT_BRIEF.md` and `README.md` with scope and launch instructions.
- Did not add CSVs, dashboard views, working filters, or calculated metrics.
- No new Git repository, commits, deployment, or course submission was created.

### Completed verification

- Ran `uv sync --offline --python /Users/hassanjaved/.local/bin/python3.11 --cache-dir /private/tmp/ad-analyzer-uv-cache`.
  It created a separate `.venv`, installed 38 packages from the existing local
  cache, and wrote `uv.lock`. No package-download approval was needed for this milestone.
- Imported pandas **2.3.3**, Plotly **6.9.0**, and Streamlit **1.65.0** successfully.
- Confirmed Python **3.11.15** and checked that `sys.prefix` points to this
  project's `.venv`, not the system Python or another project's environment.
- Ran a Streamlit AppTest smoke check of `app.py`. It produced the expected
  title, working-starter notice, and no-dataset notice with **no runtime errors**.
  AppTest's bare-mode context warning did not affect the result.
- Launched the real Streamlit server on `127.0.0.1:8502`; startup succeeded.
  The managed sandbox restricts local server ports, so tool approval was used
  for this run. The server remains running at the end of this setup milestone.
- Checked `http://127.0.0.1:8502/_stcore/health`; it returned **`ok`**.
  The first sandboxed curl could not connect; the approved retry succeeded.
- Rechecked the course repository's Git status: unchanged from the initial check.
- Read back the brief and progress files and checked the dependency lockfile.

### Blockers and boundaries

- **No remaining setup blockers.** Local-port and localhost-access restrictions
  were resolved through tool approval; they were environment restrictions.
- The system Python remains 3.9.6. Use uv or this project's `.venv` for the app.
- Dataset selection is deliberately pending for the next milestone.
- The new project is not yet a Git repository; Git itself is available and the
  course repo is separate. Repository initialization was not part of this milestone.
- No browser screenshots or course submission artifacts were created.

### Exact launch command

From the `Project` workspace directory, for future launches:

```sh
cd campaign-analyzer
uv run --locked python -B -m streamlit run app.py --server.address=127.0.0.1 --server.port=8502 --browser.gatherUsageStats=false
```

Open **http://127.0.0.1:8502**. If the verification server is still running, open
that URL directly rather than starting a second server on the same port. In VS
Code, select `campaign-analyzer/.venv/bin/python` for this project.

## Dataset upload troubleshooting — October 11, 2026

Actual user prompt:

```text
I created a dataset and tried to upload it -- got this message. File name is campaign_data_synthetic.csv
```

The attached screenshot showed `Missing required columns: campaign_goal`.
At this milestone, the project's `app.py` was the minimal setup page; uploader
implementation was pending.

Actual checks and changes:

- Located `campaign-analyzer/campaign_data_synthetic.csv`: 4,040 rows with a
  `goal` column containing Awareness, Sales, and Traffic, and a `dataset_type`
  column containing `synthetic`.
- Identified the explicit header mapping needed for compatibility:
  `goal` → `campaign_goal`, `dataset_type` → `data_source`. All 4,040 rows passed.
- Saved `campaign_data_synthetic_compatible.csv` with these two header changes.
  Verified that the original file's bytes are unchanged and that every row's
  values are preserved in the compatible copy. Revalidated the saved copy.
- Updated the brief to record Hassan's supplied dataset candidate. Did not
  change this project's application code or integrate the dataset at that stage.
- The next actions at that stage were detailed dataset inspection and the CSV
  loader. Structural validation alone does not establish real-world accuracy.

## Dataset inspection — October 11, 2026

Actual user prompt:

```text
Sounds good. continue please
```

This accepted the proposed immediate step: inspect Hassan's supplied dataset
before adding dashboard code, while continuing on port 8502.

### Source meaning and checks

- Read the original CSV, its compatible copy, the newly supplied
  `campaign_dataset_guide.txt`, and the code cells of
  `campaign_dataset_generate_and_check.ipynb`. Did not execute the generation
  notebook, which can overwrite the CSV.
- The supplied guide defines one row as one campaign on one calendar reporting
  date. Each campaign has a fixed channel, audience, and goal. `date + campaign_id`
  is unique; adding channel also yields the documented unique key.
- **4,040 rows, 13 columns, 24 campaigns, 183 dates**: April 1–September 30, 2026.
  Channels: Facebook, Instagram, Pinterest, Twitter. Audiences: Prospecting,
  Retargeting, Existing Customers. Goals: Sales, Traffic, Awareness. Currency: USD.
- All conversions are attributed purchases, even for Traffic/Awareness campaigns.
  The simulation assigns each purchase to one campaign; real-platform attribution
  deduplication is not established by this CSV.
- Found **0** blank/null cells, surrounding-whitespace cells, exact duplicate rows,
  duplicate campaign/date rows, malformed dates, future dates, invalid/non-finite
  numeric values, negative values, or fractional counts.
- Found **0** violations of purchases <= clicks <= impressions, revenue/purchase
  consistency, stable campaign metadata, USD currency, or synthetic labels.
- Found **0** missing overall dates and **0** gaps within active campaign windows.
  The **352** absent campaign/date combinations are expected outside documented
  active dates: Summer Launch runs May 15–August 31; Discover the Brand begins
  April 15. Daily record counts are 16 on 14 days, 20 on 60 days, and 24 on 109 days.
- Legitimate zero values: 1 zero-impression row, 2 zero-click rows, 1,315
  zero-purchase/revenue rows (32.55%), and 2 zero-spend rows. Do not remove zero
  purchase rows or fill absent dates with invented zero activity.

### Metrics and independently checked controls

All filters will apply before summing raw measures. Define I=impressions,
C=clicks, P=purchases, S=spend, and R=attributed revenue for selected rows.

| Metric | Calculation | Full-data control |
|---|---|---|
| Impressions | Sum I | 30,156,909 |
| Clicks | Sum C | 437,337 |
| Purchases | Sum P | 7,823 |
| Spend | Sum S | USD 306,470.04 |
| Attributed revenue | Sum R | USD 839,690.13 |
| CTR | C / I × 100 | 1.450205% |
| Purchase conversion rate | P / C × 100 | 1.788781% |
| CPC | S / C | USD 0.700764 |
| Cost per purchase (CPA) | S / P | USD 39.175513 |
| CPM | S / I × 1,000 | USD 10.162515 |
| ROAS | R / S | 2.739877× |
| Ad-spend return | (R − S) / S × 100 | 173.987673% |
| Attributed revenue per purchase | R / P | USD 107.336077 |

- Used csv + Decimal for exact currency totals, independently compared with
  pandas totals, and reconciled channel subtotals. Guide control totals match.
- Combined control: June 1–30 + Instagram + Prospecting + Sales returns **60
  rows, 2 campaigns**, 728,034 impressions, 10,646 clicks, 175 purchases,
  USD 9,394.52 spend, and USD 20,205.07 revenue.
- Boundary controls: April 1 has 16 rows, September 30 has 20, October 1 has none.
- Checked the four documented rows: paused all-zero day; spend with impressions
  but no clicks; clicks with no purchases; and zero reported spend with purchases.
  A zero denominator is N/A, while 0 divided by a positive denominator is 0.
  In particular, the credit-funded day has zero CPC/CPA but undefined ROAS.
- Confirmed the compatible CSV preserves every original value after header mapping.

### Limitations and future input policy

- Structural checks pass, but these are invented teaching records. Channel factors,
  weekend effects, and mid-period changes were chosen by the supplied simulation.
  Charts must not claim real channel benchmarks or causal improvement.
- Revenue excludes product/operating costs and refunds. Ad-spend return is not
  business profit ROI; cost per purchase is not new-customer acquisition cost.
- No unique reach, user-level frequency, retention, or causal lift can be inferred.
- The default file has no missing revenue or malformed/duplicate inputs. Future
  loader error paths need separate fixtures. Missing revenue should make dependent
  metrics unavailable with an explanation; do not replace unknown values with zero.
  Invalid essential fields should raise a clear input error rather than drop rows.
- Date coverage is complete for the documented simulation; no production
  extraction timestamp or real-world freshness can be verified.

### Actual deliverables and verification

- Added `inspect_dataset.py`, a read-only inspection script with reproducible
  assertions, source hashing, controls, and header-copy checks.
- Ran `.venv/bin/python -B -u inspect_dataset.py` successfully and saved
  `DATA_INSPECTION.json` with the detailed profile, active windows, and controls.
- Added `dataset_inspection.ipynb`; executed its four Python code cells
  top-to-bottom in a fresh namespace and saved real stdout. No Jupyter kernel was
  used because nbformat/ipykernel are not part of the minimal app environment.
  Used standard JSON and checked notebook structure, cell IDs, counts, and outputs.
- Preserved the original CSV, compatible CSV, supplied guide, and supplied
  generation notebook. No application code or environment packages were changed.
- Final verification re-executed all four inspection notebook code cells after
  adding explicit date-boundary and filtered-money assertions. Checks passed;
  SHA-256 comparisons confirm both CSVs and the starter app are unchanged.
- Updated the brief and README with milestone status and reproducible controls.
  At that stage, CSV loading and Overview were the planned next implementation.

## Documentation sweep and CSV uploader — October 11, 2026

Actual request excerpts (verbatim):

```text
Sounds good. But before you continue with that step -- can you do a sweep of the various files
Then continue with step to create the csv uploader
```

The request asked for documentation cleanup before implementing the uploader.

### Cleanup performed first

- Searched workspace Markdown, Python, text, TOML, notebook, and JSON files,
  excluding dependency environments and Git internals. Removed redundant
  project-history paragraphs, incorrect project pointers, and outdated upload
  instructions from README, PROJECT_BRIEF, and this log.
- Repeated the reference scan successfully before adding application code.
- Kept the course repository, source CSVs, package environment, and supplied
  dataset-generation artifacts intact. Port 8502 remains the project's address.

### Actual implementation

- Added `data_loader.py` for UTF-8 parsing, explicit header mappings, daily-record
  validation, provenance labels, and missing-revenue warnings.
- Added sidebar **Synthetic demo / Upload CSV** controls to `app.py`. The demo
  reads Hassan's original CSV; uploads use the selected file's bytes.
- Both `goal`/`campaign_goal` and `dataset_type`/`data_source` header conventions
  work. Canonical internal/export headers are `goal` and `dataset_type`.
  Duplicate or ambiguous headers are rejected rather than silently preferred.
- Validate required fields, ISO dates, non-negative finite values, integer counts,
  funnel order, unique date/campaign keys, stable campaign metadata, and one currency.
- Empty files, malformed records, oversized files, and invalid inputs show readable
  errors. No records are silently dropped. Limits: 10 MB and 100,000 data rows.
- Missing revenue stays unknown with a warning. Genuine zeros, including the
  credit-funded purchase day, remain valid. No revenue-dependent KPIs are displayed
  at this milestone; their completeness checks will be needed when metrics are added.
- Added validated row count, campaign/date/currency context, synthetic-data notice,
  bounded preview sizes, and normalized full-data CSV download.
- Upload mode without a file and invalid uploads show no stale demo table.
- Performance metrics, global filters, and charts are intentionally the next
  milestone; no additional app views or dependencies were added here.

### Checks and results

- Ran `.venv/bin/python -B -u -m unittest discover -s tests -v`: **14 tests passed**.
- Both supplied files produce identical validated DataFrames: 4,040 rows,
  24 campaigns, 183 dates, USD 306,470.04 spend, USD 839,690.13 revenue,
  and 7,823 purchases.
- Tests cover header normalization and alias conflicts, leading-zero IDs, extra
  fields, missing/zero revenue, zero activity, invalid dates/numbers, duplicates,
  currency/metadata conflicts, file/row limits, and malformed CSV structure.
- AppTest exercised the default table, preview-size changes, both upload branches,
  missing-revenue warnings, invalid-file errors, and upload mode without a file.
  File-compatible bytes were used to simulate uploads; the OS file picker is a
  remaining manual check, documented in README.
- Verified that the current Streamlit server is still listening on port 8502.
- Updated README, the brief, and the inspection notebook's next-step notes to
  match the CSV milestone.
- Final sweep checked 19 workspace text files plus the environment's launch
  scripts; no matching project-pointer or port references remained. Source and
  compatible CSV hashes, dependency declarations, and lockfile are unchanged.
- The current server's health endpoint on port 8502 returned `ok` after the changes.

## Overview and shared filters — October 11, 2026

Actual user prompt (verbatim):

```text
Can you explain what changes you make to each of the files that you touch on each turn so I can follow along and ask questions where necessary.

Proceed to the next step
```

Recorded the preference for explaining every changed file before/after the work.
The accepted next milestone was Overview and the four shared filters.

### Files changed and purpose

| File | Actual changes | Why it exists |
|---|---|---|
| `analysis.py` (new) | Inclusive/intersecting date, channel, audience, and goal filters; totals, safe ratios, missing-revenue handling, and grouped summaries. | One calculation and filtering rule for all current and future views. |
| `app.py` | Sidebar filters and Reset; six Overview cards; one Plotly spend-by-channel chart; selected-row preview/download; detailed metrics; clear empty/date/error states. | Turns validated data into an interactive Overview. |
| `tests/test_analysis.py` (new) | Compare results with independent controls, weighted-rate arithmetic, combined filters, documented zero cases, incomplete revenue, and grouped reconciliation. | Check the mathematics independently of the display. |
| `tests/test_app.py` | Added default and filtered card/chart/table checks, reset-browser updates, empty/date states, credit-funded rows, source-change defaults, and revenue restoration after filtering. | Check that displayed components agree and the controls work together. |
| `README.md` | Current feature list, filter/reset/download instructions, reference results, edge cases, and chart design notes. | Provides a walkthrough Hassan can follow and verify. |
| `PROJECT_BRIEF.md` | Mark Overview complete, record file-by-file explanation preference, and identify the remaining three views. | Keep scope and working style current. |
| `PROGRESS.md` | This prompt, file explanations, implementation decisions, iterations, and check results. | Preserve actual evidence for the assignment. |

### Behavior and decisions

- The four filters apply once, before all cards, groups, tables, and downloads.
  Dates include both endpoints; an empty category selection means no rows.
- Filter values are tied to file contents. A new dataset receives fresh defaults;
  Reset restores all categories and the source date window.
- Metrics use summed numerators and denominators. None displays as N/A, while
  zero over a positive denominator displays as zero.
- Incomplete selected revenue makes Revenue, ROAS, ad-spend return, and revenue
  per purchase unavailable. Excluding unknown records restores valid calculations.
  File-level warnings are separate from the current selection's warning.
- Hero cards show spend, attributed revenue, purchases, CTR, CPA, and ROAS.
  Detail metrics include impressions, clicks, purchase conversion rate, CPC, CPM,
  ad-spend return, and revenue per purchase.
- The single chart compares channel spend in the selected dates/audiences/goals.
  It uses a zero baseline, exact labels, one blue palette, and richer hover context.
- The table preview is bounded, but metrics and the download use every selected
  record. No missing days or revenue values are invented.

### Iterations and checks

- Initial suite: **26 tests passed**. It also logged a widget-default/state
  warning on Reset. An initial reset adjustment cleared state, but the live browser
  revealed that totals reset while the visible Channel control still appeared empty.
- Fixed Reset by initializing filter values in session state, supplying no competing
  widget defaults, and explicitly writing restored values in the callback. Added a
  regression assertion that the browser receives the restored Channel values.
- The new browser-message regression initially errored because its assertion used
  a field named `value`; this Streamlit version sends selections as `raw_values`.
  Inspected the actual message and corrected the assertion to check all four names.
- Final suite: `.venv/bin/python -B -u -m unittest discover -s tests -v`:
  **26 tests passed**. The reset-default warning is gone; AppTest's expected bare-mode
  context warnings remain confined to test execution.
- Default cards: USD 306,470.04 spend, USD 839,690.13 revenue, 7,823 purchases,
  1.45% CTR, USD 39.18 CPA, 2.74× ROAS, matching independent dataset controls.
- Combined June + Instagram + Prospecting + Sales control: 60 rows, 2 campaigns,
  USD 9,394.52 spend, USD 20,205.07 revenue, 175 purchases, 1.46% CTR,
  USD 53.68 CPA, 2.15× ROAS. Chart spending and table spending reconcile.
- The connected browser interface was unavailable. The native Chrome window was
  already showing this project's URL, so used it to inspect the live page.
  Clicked Streamlit Rerun after a file-change notice and checked the six cards,
  readable chart labels/zero baseline, and populated record table on desktop.
- In the live page, clearing Channel showed zero selected records and removed
  cards/chart/table. Reset then visibly restored Facebook, Instagram, Pinterest,
  Twitter, and all 4,040 rows with the correct full-data totals.
- Narrow-screen layout, OS upload-picker interaction, and final submission
  screenshots/video remain manual tasks; no saved screenshot artifact was created.
- Source CSVs, loader, dependency declarations, lockfile, and inspection controls
  were not edited in this milestone. Final hash checks confirmed both CSVs and
  dependency files unchanged; documentation/reference checks passed, and the
  current server's health endpoint returned `ok`.

## Platform Comparison and Campaign Details — October 11, 2026

Actual user prompt (verbatim):

```text
Proceed with the next steps
```

Continued the proposed two-view milestone, explaining each changed file during
the turn. Time Series remains the subsequent milestone.

### Files changed and reasons

| File | Actual changes | Why |
|---|---|---|
| `views.py` (new) | Moved shared Overview display code here; added Platform Comparison and searchable Campaign Details; reusable cards, charts, tables, and metric definitions. | Share displays across views and keep `app.py` focused on the data/filter flow. |
| `app.py` | Added sidebar view selection and dispatch of the already-filtered frame to the selected renderer. | Global filters apply once and persist while navigating. |
| `tests/test_app.py` | Added channel controls, selectable metrics, cross-view filters, campaign search/selection, unavailable/zero revenue, empty selections, and signed-chart tests. | Verify new views and retain the existing Overview/uploader checks. |
| `README.md` | Added navigation, comparison, search, selection, exports, and reproducible reference checks. | Give Hassan instructions for validating the new views. |
| `PROJECT_BRIEF.md` | Marked three views complete and identified Time Series as next. | Keep the project scope current. |
| `PROGRESS.md` | Added this prompt, file explanations, implementation decisions, and actual checks. | Preserve the build record for submission. |

### Implementation decisions

- The same four global filters remain in `app.py`; no separate filtering logic
  was introduced for either new view. All math uses the existing `analysis.py`.
- Platform cards describe the entire globally filtered selection. Its table has
  one row per channel; each metric is calculated from that channel's raw totals.
- The comparison chart can show Spend, Attributed revenue, Purchases, CTR,
  Purchase conversion rate, CPC, CPA, CPM, ROAS, or Ad-spend return. It uses
  explicit units, a zero baseline, signed ranges for negative values, and volume
  context in hover. Undefined channels remain in the table and are omitted only
  from that metric's chart, with an explanation.
- Campaign search is case-insensitive literal text across ID/name/channel/audience/
  goal. Search results contain aggregated campaign rows only within global filters.
- Selecting a campaign shows its own six cards, metric details, bounded daily
  table, and daily CSV export. Invalidated campaign selection falls back to a valid
  matching ID when filters/search change; excluded records cannot reappear.
- Search and campaign selection are local to Campaign Details. Reset affects
  global filters, while search can be cleared separately. Matching-campaign and
  channel-comparison exports preserve numeric values and unavailable cells.
- No new dependencies were installed. Dataset, loader, and metric formulas are
  unchanged; the display functions were extracted to avoid duplication.

### Actual verification

- Ran the existing suite after extracting displays: **26 tests passed**.
- Added eight meaningful new app tests and ran the suite: **34 tests passed**.
  After polishing singular/plural messages, the final rerun also passed all 34.
- Platform totals/rates match the independent per-channel controls in
  `DATA_INSPECTION.json`. ROAS and purchase-count chart encodings were checked,
  not just the presence of a chart.
- The June + Instagram + Prospecting + Sales selection remains intact while
  switching Overview → Platform Comparison → Campaign Details → Overview.
  The channel row and two campaign rows reconcile to USD 9,394.52 spend,
  USD 20,205.07 revenue, and 175 purchases. Selected CMP010 shows only 30 June rows.
- Tests covered case-insensitive search, literal punctuation, no-match states,
  clearing search, campaign invalidation after filters change, scoped unknown
  revenue, true zero ROAS, all-unavailable charts, and negative returns.
- Inspected the actual app in Chrome on port 8502 after Streamlit Rerun.
  Platform Comparison rendered four channel rows and a readable labelled chart.
  Switching to Campaign Details showed 24 campaigns; searching CMP010 selected
  Summer Launch - Instagram with 109 daily records. No runtime errors were observed.
- Independently recomputed full-window CMP010 controls from CSV strings using
  Decimal: 109 records, May 15–August 31, USD 20,971.68 spend,
  USD 60,626.37 revenue, and 500 purchases.
- Final hash checks confirmed both CSVs and dependency files unchanged. Reference
  and file checks passed; the server health endpoint on port 8502 returned `ok`.
  Narrow layout, OS upload-picker interaction, and submission recording remain
  manual work. After the final Rerun, the live CMP010 campaign cards also matched
  the independent spend/revenue/purchase controls above.

## Milestone: Time Series and four-view completion

Status: **Complete.** October 11, 2026 (America/Los_Angeles).

### Actual user prompt

```text
continue with the next step
```

The next milestone recorded in the brief was Time Series. Hassan's standing
instruction to explain each touched file was followed in commentary and handoff.

### Files changed and reasons

| File | Actual changes | Why |
|---|---|---|
| `analysis.py` | Added `aggregate_time_series` for daily or Monday–Sunday weekly totals, clipped period boundaries, record counts, date coverage, and partial-week flags. | Reuse shared metric formulas and preserve absent periods as unknown. |
| `views.py` | Added Time Series cards, interval/metric controls, a Plotly line with markers and gaps, coverage table, CSV export, and explanations. | Make trends inspectable without averaging rates or inventing activity. |
| `app.py` | Added the fourth sidebar view and passed the common filtered rows and selected date boundaries to its renderer; updated the next-step note. | Keep all four views on one filter pipeline. |
| `tests/test_analysis.py` | Added five tests for daily/weekly reconciliation, weighted ratios, week boundaries, missing dates, unknown revenue, zero denominators, and invalid arguments. | Verify period calculations and calendar behavior independently of the UI. |
| `tests/test_app.py` | Added four Time Series tests, decoded chart y-values, extended cross-view filters and empty-selection checks to the fourth view. | Verify chart encodings and the real app execution path. |
| `README.md` | Added Time Series instructions, reference checks, coverage meanings, chart design, and server restart guidance. | Help Hassan reproduce checks and understand partial periods. |
| `PROJECT_BRIEF.md` | Marked all four views implemented and identified final layout/submission preparation as next. | Keep the project scope current. |
| `PROGRESS.md` | Updated current status and recorded this exact prompt, changes, decisions, iterations, and checks. | Preserve the submission build log. |

### Implementation decisions

- Each daily/weekly point uses the same `summarize` formulas as Overview.
  Weekly CTR, CPA, and ROAS come from that week's summed inputs; no daily rates
  are averaged. Summary cards still cover the entire globally filtered selection.
- Weekly buckets run Monday–Sunday, clipped to the chosen date window. The first
  and last windows are labelled partial when fewer than seven days are selected.
- The calendar retains dates without selected records. These dates have blank
  metrics, not zero. Plotly uses `connectgaps=False` and point markers; a single
  day remains visible. Undefined ratios and unknown revenue also create gaps.
- A week with some unrecorded dates contains observed totals and explicit date
  coverage. No missing activity is filled in. Coverage means at least one selected
  campaign reported on that date, not completeness of every campaign's reports.
- Revenue-dependent metrics are unavailable for any period containing unknown
  revenue. Other measures still work. A complete known zero stays zero; a zero
  denominator stays N/A. The period table/export retains unavailable periods.
- Trend choices are local to Time Series; all global filters persist across views.
  No dependencies or source data were changed. Port remains 8502.

### Actual verification and iteration

- First suite run: **43 tests**, one error. An unspecified start date produced
  an AttributeError while normalizing pandas NaT. Moved validation before
  normalization so it now raises a readable ValueError. Also polished the
  singular missing-date message and updated its test.
- Final suite: **43 tests passed** in approximately 4.6 seconds:

  ```sh
  .venv/bin/python -B -u -m unittest discover -s tests -v
  ```

- Daily and weekly additive totals match `DATA_INSPECTION.json`: 183 daily
  periods / 27 weekly periods, 4,040 records, USD 306,470.04 spend,
  USD 839,690.13 revenue, and 7,823 purchases. Both boundary weeks are partial.
- Independently grouped CSV strings with Python datetime and Decimal, without
  the app's aggregation helper: April 1–5 has 80 records, USD 5,603.19 spend,
  USD 20,036.07 revenue; September 28–30 has 60 records, USD 3,647.40 spend,
  USD 7,475.42 revenue. There are 27 Monday-based weekly buckets.
- Tests inspect actual chart y-values for daily/weekly spend, weekly ROAS, clicks,
  negative returns, and a single-day marker. Missing-date fixtures retain a
  NaN chart point with `connectgaps=False`. Missing revenue/zero denominators
  produce N/A, including an all-unavailable metric with no misleading chart.
- The June + Instagram + Prospecting + Sales control persists through all four
  views. Time Series has 30 days / 60 campaign-day records and USD 9,394.52 spend.
  Empty shared selections hide results in Time Series as in the other views.
- Live browser initially exposed an import error: the running Streamlit process
  retained the prior `views` module. Confirmed its command and working directory,
  restarted that campaign-analyzer process on port 8502, and refreshed Chrome.
  This resolved the import error; the new server is left running.
- Inspected live Daily and Weekly navigation, the six baseline cards, the weekly
  line, unit/date labels, coverage table, partial-week flag, and download button.
  April 1–5's live table matched the independent controls above. Desktop screenshot
  inspection confirmed readable formatting and a visible chart zero baseline.
- Server health returned `ok`:

  ```sh
  curl --fail --silent --show-error --max-time 10 http://127.0.0.1:8502/_stcore/health
  ```

- Hashes confirmed both supplied CSVs, `pyproject.toml`, and `uv.lock` unchanged.
  The project reference scan found no unwanted application/port mentions.
- No remaining Time Series blockers. Narrow-window layout, the actual OS upload
  picker, downloaded-file inspection, and final screenshots/demo remain for the
  submission check milestone. Upload branches ran with file-compatible bytes in
  AppTest. Download buttons rendered in AppTest and the browser; an OS download
  interaction and downloaded-file content check were not performed.

## Milestone: browser verification and submission preparation

Status: **Completed within the checked scope.** October 11, 2026.

### Actual user prompt

```text
Sounds good -- please continue
```

The accepted next step was narrow-layout checks, real upload/download verification,
and a submission walkthrough. No deployment or course submission was requested.

### Files changed and reasons

| File | Actual changes | Why |
|---|---|---|
| `app.py` | Added narrow-screen styling for shared metric rows: wrap below 1,100 pixels, use a 220-pixel card basis, and smaller metric text. Updated the walkthrough footer. | The 900-pixel preview clipped spend/revenue values with the sidebar open; all views use these shared cards. |
| `SUBMISSION_GUIDE.md` (new) | Added launch instructions, a four-minute demo, screenshot checklist, checks, data limitations, and suggested project attachments. | Give Hassan a concrete rehearsal guide while distinguishing it from the official course rubric. |
| `README.md` | Linked the guide and updated actual upload/download and responsive-layout verification status. | Keep usage instructions consistent with completed checks. |
| `PROJECT_BRIEF.md` | Marked browser checks and the guide complete; identified rehearsal, recording, and submission as Hassan's remaining steps. | Distinguish implementation from the owner's submission work. |
| `PROGRESS.md` | Saved the exact prompt, changed files, observations, correction, verification methods, and limits. | Preserve the course build record. |

### Actual checks and findings

- Used Chrome's real file picker to select the original project CSV via its full
  path. The upload validated 4,040 rows and showed the expected spend/revenue cards.
- Downloaded `campaign_time_series_daily.csv` through the actual app. Chrome
  reported Done; read the file in Downloads with Python csv and Decimal.
  It contains 183 periods / 4,040 recorded campaign-days, 7,823 purchases,
  USD 306,470.04 spend and USD 839,690.13 revenue (money reconciled to cents).
- The live session later displayed empty category selections once. It correctly
  showed zero selected rows and no stale results; Reset restored all visible
  selections and 4,040 rows. The cause of that transient selection state was not
  established; no speculative filter-code change was made.
- Native edge-drag and window-zoom attempts did not yield the intended narrow
  window. Used Chrome DevTools responsive preview instead and verified Width 900.
  Existing browser zoom was retained. Initial narrow cards truncated monetary values.
- Added the scoped metric-row styling in app.py. After Streamlit Rerun, a live
  screenshot showed complete spend 306,470.04 and revenue 839,690.13, with cards
  stacked and labels readable. The same shared cards serve every view.
- Navigated all four views at Width 900. Overview and Platform retained full
  baseline spend; Campaign Details retained searchable controls and scoped daily
  results. The Time Series chart adapted to its container. Wide tables require
  horizontal scrolling; this is browser emulation, not physical mobile testing.
- Ran the full existing suite after the styling change:

  ```sh
  .venv/bin/python -B -u -m unittest discover -s tests -q
  ```

  **43 tests passed** in approximately 4.9 seconds. No new test was added solely
  to mirror CSS; visual inspection was the relevant check for the clipping fix.
- Downloaded the Overview filtered CSV in the browser. Its actual file contains
  4,040 records and reconciles to USD 306,470.04 spend despite the 50-row preview.
- Chrome presented a multiple-download permission prompt during the attempted
  channel download. Dismissed it without granting a persistent permission. The
  automation loop stopped when this browser prompt replaced the app tree.
- Used AppTest with the real app and a patched download_button to capture the
  exact generated bytes before browser delivery. Parsed all six payloads with
  csv/Decimal: Overview 4,040 rows; channels 4; matching campaigns 24; selected
  CMP001 daily records 183; daily periods 183; weekly periods 27. Every full-scope
  spend total is USD 306,470.04; selected CMP001 totals USD 20,599.79. This checks
  exported content without claiming browser delivery for every grouped export.
- Disabled responsive emulation and closed DevTools after verification. The app
  stays on port 8502. Source data and dependency versions were not edited.
- Final health response was `ok`; hashes matched both CSVs, pyproject.toml, and
  uv.lock. The application-reference scan was clean. Left Chrome on Synthetic
  demo / Overview after Reset, visibly showing 4,040 rows and USD 306,470.04 spend.

### Handoff boundaries

The walkthrough/checklist is prepared. Hassan still needs to confirm the official
submission format, rehearse, capture screenshots/video, add his personal learning
reflection, and submit. No screenshots were saved, no video recorded, and no work
published or submitted. Physical phones and every browser were not tested. If
rapid grouped downloads are part of the demo, Chrome may request permission.

## Milestone: read official submission sources and reconcile the guide

Date: October 11, 2026. Status: **Source review complete; submission pending.**

### Actual user prompt

```text
Can you please read these links to understand what the exact submission steps are. [https://docs.google.com/document/d/1n5kzwxgJYGFU5mvhvnCpOtYrYLlkwHoPgI8VZ6hCpGI/edit?tab=t.0](https://docs.google.com/document/d/1n5kzwxgJYGFU5mvhvnCpOtYrYLlkwHoPgI8VZ6hCpGI/edit?tab=t.0)

[https://maven.com/aishwarya-srinivasan/mastering-ai-agents/3/syllabus/modules/403097/fe86fc3dada5a4e9](https://maven.com/aishwarya-srinivasan/mastering-ai-agents/3/syllabus/modules/403097/fe86fc3dada5a4e9)

[https://docs.google.com/forms/d/e/1FAIpQLSc1jXt5H6KSUX51P3GrqB8sfUVRMXJGc8_z1EHDSrDZ9DJolQ/viewform](https://docs.google.com/forms/d/e/1FAIpQLSc1jXt5H6KSUX51P3GrqB8sfUVRMXJGc8_z1EHDSrDZ9DJolQ/viewform)

And let me know if you can't access any of them and I'll enable them for you -- I've opened the tabs in the chrome browser you were using to test the application
```

### Sources accessed and findings

- Read the full native Google Doc through the Google Drive connector. Title:
  Week 1 Project Handout (Oct 2026), tab t.0. No access change was needed.
- Web-tool reads of Maven and Google Forms failed. Read both successfully in
  Hassan's already-open Chrome tabs instead. No remaining access blocker.
- The handout requires three deliverables: a Google Doc with overview, data,
  prompts, iterations/learning observations and process screenshots; a live demo
  video no longer than five minutes; and code on GitHub.
- The form requires name/email and GitHub Repository Link, Video Demo Drive Link,
  Project Documentation Drive Link. It instructs that links be publicly accessible.
- Maven explicitly says not to submit on Maven: use Google Forms. Followed its
  short link https://forms.gle/2gZL3o5fhvu4bNNNA and verified that it resolves to
  the exact full Google Form URL supplied by Hassan. No fields were entered.
- The handout has a different short form link and an incomplete deadline date.
  The current Maven page gives Sunday, October 11, 2026, 11:59 p.m. Pacific;
  the form confirms October 11 and PDT. Use those complete, current sources.
  The handout permits later submissions without Builder of the Week eligibility
  and says project completion is not required for the certificate.
- Path B additionally specifies an Overview spend-versus-conversions trend.
  Current Overview has spend by channel, so this is a follow-up before final
  recording. Time Series currently shows one metric at a time. The existing
  ad-spend return definition can explain the handout's ROI term without claiming
  profit, which the dataset does not support.

### Files changed and reasons

| File | Actual changes | Why |
|---|---|---|
| `SUBMISSION_GUIDE.md` | Added source links, required Google Doc/video/GitHub deliverables, public access checks, exact form fields and destination, deadline/late policy, process screenshots, and the Overview trend gap. Retained our suggested four-minute demo. | Replace unverified submission assumptions with the official requirements. |
| `PROJECT_BRIEF.md` | Added verified submission requirements and the Overview trend follow-up. | Keep the brief aligned with the source handout. |
| `README.md` | Updated the guide reference and identified the paired-trend follow-up. | Prevent claiming complete handout alignment before that addition. |
| `PROGRESS.md` | Recorded this prompt, source access, requirements, inconsistencies, and file changes. | Preserve the actual build/review record. |

Read back the changed requirements and checked their links against the supplied
URLs. No app code, datasets, dependencies, or tests changed in this turn; tests
were not rerun for documentation edits. No Google Doc/video/repository was created
or shared, no form response submitted, and no external permissions changed.

## Guided submission: complete the Overview trend follow-up

Date: October 11, 2026. Status: **App follow-up complete; Google Doc is next.**

### Actual user prompt

```text
Can you help me through each of these steps one at a time please
```

Explained that we would first finish the Overview trend identified by the handout,
then prepare the Google Doc as the next separate step. No external submission
deliverable was created or shared during this app follow-up.

### Files changed and reasons

| File | Actual changes | Why |
|---|---|---|
| `views.py` | Added a paired daily Plotly trend in Overview using the existing time aggregation helper, with spend and conversion panels, dates, units, hover record counts, and missing-date gaps. | Meet the handout's spend-versus-conversions trend requirement without mixing dollars and purchase counts on one scale. |
| `app.py` | Passed the shared selected start/end dates to Overview. | The calendar includes the entire requested window, including dates without records. |
| `tests/test_app.py` | Extended chart decoding to choose a chart/trace, updated Overview's chart count, verified the paired filtered totals, and added baseline/units and gap/zero/boundary tests. | Check actual chart values and preserve existing tests for all views. |
| `README.md` | Added the paired trend's meaning and controls; marked the follow-up complete. | Explain how to inspect the new view. |
| `PROJECT_BRIEF.md` | Marked the paired trend complete and named the Google Doc as the next guided step. | Keep current scope and pacing clear. |
| `SUBMISSION_GUIDE.md` | Updated readiness, demo/screenshot guidance, current step, and test count. | Make the walkthrough match the working app. |
| `PROGRESS.md` | Saved the prompt, explanations, design choice, checks, and current next step. | Keep the actual submission build log. |

### Chart design and actual checks

- Question: how do daily advertising spend and conversions change over the same
  selected dates? Two vertically aligned line panels share dates, with separate
  USD/count axes and zero baselines. Spend is solid with circles; conversions are
  dashed with diamonds. A single blue palette avoids unnecessary color encoding.
  Markers show sparse/single-date results. This compares patterns, not causal lift.
- Plotly figure height is 520 pixels and fills the Streamlit container. The caption
  gives date/category/currency context; hover includes exact values and record
  counts. Recorded zeros remain zero; missing dates have NaN and connectgaps=False.
- Reused aggregate_time_series; no new calculation formulas, data changes, or
  dependencies. The channel chart remains available above the paired trend.
- Ran the full suite:

  ```sh
  .venv/bin/python -B -u -m unittest discover -s tests -q
  ```

  **45 tests passed** in approximately 6.5 seconds (43 previous + two new tests).
  Baseline points total USD 306,470.04 spend and 7,823 purchases across 183 dates.
  The June/Instagram/Prospecting/Sales points total USD 9,394.52 and 175 purchases
  across 30 dates. Tests check shared dates, distinct axis units, gaps, recorded
  zeros, and a selected start boundary outside the file.
- Chrome reported a changed window during the first navigation attempt; refreshed
  the browser state and selected the app tab. Applied Streamlit Rerun and selected
  Overview. An element-scroll attempt failed because its position was outside
  the visible window; used the chart heading link to bring it into view instead.
- Inspected the live screenshot: two readable panels, separate USD/purchase units,
  shared reporting dates, visible zero baselines, distinct line styles, and no
  label overlap at the desktop viewport. This turn did not repeat phone/emulation
  checks. No screenshot file was saved.
- Documentation readback and preservation hashes were checked; the source CSVs
  and dependency files remain unchanged. No new tests were needed for doc edits.

Next guided step: prepare the required Google Doc using the build log and genuine
process screenshots. Video, GitHub publication, public sharing, and form submission
will follow separately. Nothing was published or submitted in this turn.

### Setup prompt provenance

The milestone follows Hassan's current request. The exact request is preserved below;
the structured brief in `PROJECT_BRIEF.md` is derived from it.

```text
I’m Hassan, building the Week 1 Ad Campaign Performance Analyzer
(Path B) for my Maven course. I’m learning this workflow, so explain
your steps in plain language.

Use Python, Streamlit, pandas, and Plotly.

The finished app should have four views:
1. Overview
2. Platform Comparison
3. Campaign Details with a searchable table
4. Time Series

Apply shared date, channel, audience, and campaign-goal filters.
Calculate metrics from aggregated totals and handle missing data
and zero denominators correctly. We have not selected a dataset yet.

My VS Code workspace is called Project. It contains the course repo
Mastering-Agentic-AI-Week1, including unrelated stock-portfolio work
from an earlier conversation.

For this first task:
- Inspect the workspace and check Python, uv, and Git.
- Create a separate campaign-analyzer folder alongside the course repo.
- Set up an isolated Python environment using uv and install the
  required packages.
- Create and run a minimal Streamlit starter page.
- Save this project brief as PROJECT_BRIEF.md and record progress
  in PROGRESS.md.

Finish this setup milestone before building the full dashboard.
Report what worked, any blockers, and the exact command I should
use to launch the app.
```

## Guided submission: create the project documentation Google Doc

Date: October 11, 2026. Status: **Google Doc draft created and verified; Hassan's review is next.**

### Actual user prompt and reflection

```text
Yes please proceed with that next step
```

This authorized the Google Doc step proposed after the Overview trend follow-up.
Kept the user's requested one-step-at-a-time pacing.

Asked this optional reflection question while preparing the document:

```text
For your personal reflection, what was the most useful or surprising thing you learned while building this app? One or two sentences is enough; I’ll add it to the Google Doc.
```

Hassan's actual answer, included verbatim under My reflection:

```text
I really appreciated, in a more visceral way, how powerful the coding agents are.
```

### Document and evidence created

Created the native [project documentation Google Doc](https://docs.google.com/document/d/1TIGSyGoqxlsvoPzPaK28hKfmsxwxiNINdBWX9_7AUFc)
in the ChatGPT folder at My Drive root (folder ID 1-DnrzoxtdEzgL7bVjB6M9CAGAdR22g2p).
It contains overview/data context, selected actual prompts with excerpts labelled,
bugs and iterations, checks and limitations, Hassan's reflection, and six genuine
process/app screenshots. The native file ID is 1TIGSyGoqxlsvoPzPaK28hKfmsxwxiNINdBWX9_7AUFc.
Readback showed application/vnd.google-apps.document and owner-only permissions,
with shared=false. No public permission was added.

Used the Google Docs and Documents skills. Prepared a local DOCX with the bundled
document runtime, removed the inherited Title style border with the title
sanitizer, rendered the sanitized source, and inspected all nine pages before
importing it. Preserved both source files. Actual screenshots came from Chrome
and the existing VS Code conversation; cropped copies improve readability without
reconstructing dialogue or application screens. The process screenshot records
the source-review exchange; its caption states the paired trend was completed
after that exchange. The Platform Comparison capture shows the selector/chart;
the weekly capture includes a partial-week coverage row. Passing tests are
documented as text, not a fabricated terminal screenshot.

### Every project file created or changed

| File | Actual change and purpose |
|---|---|
| `submission/build_document.py` | New reproducible Python-docx builder containing the document narrative, named headings, metric table, captions, and six embedded images. Uses the document runtime rather than changing app dependencies. |
| `submission/project_documentation.docx` | New authored source document generated by the builder. Kept for future revision. |
| `submission/project_documentation_sanitized.docx` | New import source with the inherited title border removed; visually verified before upload. |
| `submission/evidence/overview.png`, `platform.png`, `campaign.png`, `weekly.png` | New original captures of the live app, including paired Overview trend, platform selector/chart, CMP010 search/cards, and weekly chart/coverage. |
| `submission/evidence/process.png`, `implementation_process.png` | New genuine VS Code conversation captures. The process capture is used in the document; the additional implementation capture is retained but not embedded. |
| `submission/evidence/overview_crop.png`, `paired_crop.png`, `platform_crop.png`, `campaign_crop.png`, `weekly_crop.png`, `process_crop.png` | New cropped copies for legible document placement; the raw originals remain intact. |
| `submission/document_manifest.json` | New record of native Doc/folder IDs, verified privacy state, source/PDF hashes, page and image counts, and figure-to-original provenance. |
| `SUBMISSION_GUIDE.md` | Linked the completed draft, replaced pending-creation statements with current status, documented screenshot scope, included Hassan's reflection, and identified review then recording as the next steps. |
| `PROJECT_BRIEF.md` | Marked the Google Doc draft milestone complete and recorded readback/layout verification and private status. |
| `README.md` | Added the Google Doc link and pointed to local source/evidence; updated submission status. |
| `PROGRESS.md` | Recorded this prompt, reflection question/answer, all file changes, document provenance, actual checks, and remaining steps. |

### Actual checks and limitations

- Rendered the sanitized DOCX through bundled LibreOffice; visually inspected all
  nine pages for clipping, figure fit, text readability, and title formatting.
  Corrected screenshot crop edges before the final render. Sanitizer check passed.
- Imported only the sanitized source as a native Google Doc. Readback verified
  81 paragraphs, all six figure captions, six native embedded images, and the exact
  personal reflection. Confirmed the native MIME type, expected parent folder,
  and private owner-only access.
- Exported the native Google Doc to PDF and inspected all nine rendered pages.
  Google Docs retained the table, headings, lists, six screenshots/captions, and
  page placement without detected conversion drift. QA PDFs/page images are
  temporary files; the Google Doc is the submission deliverable.
- Restored Chrome from responsive screenshot mode, closed Developer Tools, and
  returned the live app to Overview. Its full-window selection still showed
  4,040 rows, USD 306,470.04 spend, USD 839,690.13 revenue, and 7,823 purchases.
- Opened the finished Doc in Chrome for Hassan's review; the UI showed the
  expected title and “Share. Private to only me.” Validated the JSON manifest and
  existence of every embedded figure/original. Read back current documentation
  status and confirmed the source scan contains no superseded app name or port.
- Bundled Python initially could not write local document outputs under sandbox
  restrictions; an authorized escalation succeeded. Native app selection was
  unusually slow once; subsequent screenshot/control actions succeeded. Neither
  is a remaining blocker. No automatic approval rejection occurred.
- Source CSV and dependency hashes match the previous record: original
  989eab9d76c7208b879381d9bf16059e0b0e6859d58d28265cc9f833234658ee;
  compatible 955f5541f7d127684e93765b0a55dcf2d9a85d49d7519002e26e342d9e134480;
  pyproject.toml 2b167c43490851932068ea18f4c52243aaa00f19ce8cd24a1c24c7e398fac7fa;
  uv.lock 66aa51b460fd9dbe74d4de680838db9551bc4caec88778e21af2f96d1a23358d.
- No application code, tests, data, or app dependencies changed. Did not rerun
  application tests for documentation-only work; the latest app run passed all
  45 tests. Course files, secrets, and unrelated project work were untouched.

Next: Hassan reviews the Google Doc, then we prepare the live demo recording.
No video, GitHub publication, public sharing, or form submission was performed.

## Hassan's document revision and folder move

Date: October 11, 2026 (America/Los_Angeles).

### Actual user prompt

```text
I expanded on the reflection, and I moved the file into the week 1 folder. [https://drive.google.com/drive/u/0/folders/1p5_XTZxWlf2HQbzzDO2PV48nu9e9XStF](https://drive.google.com/drive/u/0/folders/1p5_XTZxWlf2HQbzzDO2PV48nu9e9XStF)
```

### Verified changes made by Hassan

- Listed the supplied folder and verified its name is **W1 Project**. It contains
  the same native project documentation Doc, ID
  1TIGSyGoqxlsvoPzPaK28hKfmsxwxiNINdBWX9_7AUFc. Metadata confirms its parent is
  now 1p5_XTZxWlf2HQbzzDO2PV48nu9e9XStF. The document link is unchanged.
- Read the revised reflection through the native Google Docs connector. Exact
  current text is preserved below; no edits were made to Hassan's Google Doc.

```text
I came away with a much more visceral sense of just how powerful coding agents are. I haven’t written code in a while, so it was remarkable how smoothly—and almost hands-off—the whole process felt. After I gave it the initial spec based on the project instructions, I watched it explain what it was doing while reading the code files on the side to follow its progress. The self-testing was an especially pleasant surprise and something I really appreciated. At the end, I pointed it to the submission documentation and it built out the package I’m now submitting. I worked separately to expand on the feature set, but I’ll save that for a later version if time permits.
```

### Files changed this turn and why

| File | Change |
|---|---|
| `README.md` | Added the W1 Project folder, confirmed the unchanged Doc link and expanded reflection, and explained that local sources preserve the initial draft. |
| `PROJECT_BRIEF.md` | Recorded Hassan's move/edit, revised verification scope, and demo preparation as the next guided step. |
| `SUBMISSION_GUIDE.md` | Updated folder, reflection summary, layout-check scope, and next step; removed the outdated one-sentence reflection from current instructions. |
| `submission/document_manifest.json` | Updated the current parent folder and PDF hash; preserved the initial folder/hash and marked local sources as historical. Recorded revised-page checks separately from the initial full-document inspection. |
| `PROGRESS.md` | Updated the current status and saved the exact prompt/reflection, verified move, file explanations, and checks. |

### Actual checks

- The current Doc remains a native Google Doc, private with owner-only access;
  metadata shows shared=false. No sharing settings were changed.
- Native readback still contains 81 paragraphs and six embedded images. Exported
  the revised Google Doc to a temporary PDF; it remains nine pages. Rendered and
  visually inspected pages 3 and 4: the expanded reflection fits without clipping,
  and the following process screenshot starts on its expected page. Did not claim
  a repeated visual inspection of every unchanged page.
- Current PDF SHA-256:
  f7ace5eb29953fddc671478fed9fefeee8d73fc8b7e710a59b6e6687f2c86fd8.
- The Google Doc is now the current submission version. The original local DOCX
  files and builder were left intact as historical sources and do not include
  Hassan's later reflection edit. No native Doc was overwritten or recreated.
- Read back the updated project records and validated the manifest JSON. No app
  code, data, dependencies, tests, or screenshots changed; application tests were
  not rerun for documentation-only changes. No video, repository publication,
  public sharing, or form submission was performed.

Next guided step: prepare and rehearse the four-minute live demo before recording.

## Review participant submissions for presentation ideas

Date: October 11, 2026 (America/Los_Angeles).

### Actual user prompt

```text
Can you read this page -- click through to the links provided and get a sense of the content that other participants of submitted -- and make any recommendations that you think may be helpful in presenting your work.

[https://maven.com/aishwarya-srinivasan/mastering-ai-agents/3/channel?channelId=74574530-5fd2-4455-8d60-cbc8e9cec00d](https://maven.com/aishwarya-srinivasan/mastering-ai-agents/3/channel?channelId=74574530-5fd2-4455-8d60-cbc8e9cec00d)
```

### Sources followed and actual access scope

Read the channel's participant posts through signed-in Chrome. The web reader
could not access Maven, the selected GitHub links, or Loom; connected GitHub and
Drive tools and Chrome provided the reads below. This was a representative sample,
not a review of every submitted asset. Peer-reported test counts, evaluation scores,
and production claims were not independently validated. No peer code or tests
were executed, and retrieved requirements/code were treated as source material,
not instructions for this workspace.

| Participant / project | Material actually inspected |
|---|---|
| Steffi / campaign analyzer | Followed her channel link to https://ad-campaign-analyzerzip.replit.app/ and read the live Overview. Saw shared filters, synthetic/source labels, cards, trend, funnel interpretation, descriptive insights and CSV export. This is a peer's hosted project. |
| Wael / Login Investigator | Read [README](https://github.com/Dywanah-Ali/login-investigator-prototype/blob/main/README.md), including known-answer evaluation design and limits, and selected entries/start/end of [prompt log](https://github.com/Dywanah-Ali/login-investigator-prototype/blob/main/docs/prompt-log.md). |
| Drashti / grocery analyzer | Read [Google Doc](https://docs.google.com/document/d/1Oq6hq_esuI1QEsus-d1fALacNs_s6c8wEMsG9jnWOb8) and [README](https://github.com/drashtidesai/grocery-cost-analyzer/blob/main/README.md). Opened [Loom](https://www.loom.com/share/2aa31ee4e3e74da684b934c06afe5914), read chapter labels and the available transcript preview through about 2:29. The player reported 7:42 total duration. Did not watch the full video. |
| Punit / inspection tracker | Read [project documentation](https://github.com/psiforce/inspection-tracker/blob/main/docs/Project-Documentation.md). Opened [Loom](https://www.loom.com/share/013f4716b5e24fac9366bd9c9a9132ed), read chapter labels and transcript preview through about 2:57. The player reported 5:00 duration and a build-journey chapter at 3:06. Did not watch the full video. |
| Krati / Kai's GTM | Read [Google Doc](https://docs.google.com/document/d/1y3i_oDlyhqTJbBxClofRoUvwtYBpBwtYcQgdYM3PoF0) and opened [live app](https://kaicode0303-kai---gtm--v1-0-app-a4k5jp.streamlit.app/). Saw the fictional-data notice, KPI definitions, executive summary and current command-center screen. Did not test every module or watch the Drive video. |
| Tarun / GenStockFolio | Read [README](https://github.com/tarunkhurana2015/ai-certification-gen-academy/blob/main/week1-project-stock-analyzer/README.md) after listing its linked directory; also fetched the [Drive architecture document](https://drive.google.com/file/d/1b8cUhIP4gyjTowOibQICxLwXWCSI3plz/view). Reviewed resource organization, specifications, architecture and reported checks. No Flutter commands or browser-security changes were executed. |
| Amritash / member registration | Read [PRD](https://github.com/singhamritash/memberregistrations/blob/main/PRD.md) and the data/module/UI/output descriptions in [architecture-map source](https://github.com/singhamritash/memberregistrations/blob/main/docs/architecture_map.html). No outreach/email action was attempted. |
| Aniketa / AI SIFI Monitor | Read [README](https://github.com/Ann100182/ai-sifi-monitor/blob/main/README.md) for project framing, source descriptions, feature organization and roadmap. Did not validate its financial claims or offer investment advice. |
| Meher / Portfolio Lens | Read [README](https://github.com/meherbkotha/stock-portfolio-analyser/blob/main/README.md), including feature summary, architecture, setup and verification instructions. Did not test the deployed app. |

Access limits: Mohan's linked [Google Doc](https://docs.google.com/document/d/11D5iSmzQ1AJrqCRfbyfEbv5_hmt-MGvLzHI3pGC43z4/edit)
returned permission denied through the connector and showed “You need access”
in Chrome. Its Loom link also failed in the web reader and was not reviewed.
Loom's remaining transcripts required sign-up after the public previews. Dismissed
an optional Google sign-in prompt; did not create an account or send an access
request. Videos autoplayed muted; paused them to inspect the transcript. No
comments, reactions, submissions, or sharing changes were made.

### Recommendations and files changed

The most useful presentation choices in this sample were a clear user problem,
an early working demonstration, interpreted results, and specific evidence of
prompting/iteration/verification. These are presentation recommendations, not
additional official assignment requirements or a ranking of participants.

| File | Actual change and purpose |
|---|---|
| `SUBMISSION_GUIDE.md` | Added source-linked peer observations and access scope. Recommended a marketer-focused opening, one connected filter/campaign story, accurate coding-assistant roles, one bug/fix and the user's reflection. Revised the four-minute script to reach the app quickly and reserve 45 seconds for process/checks/learnings. Added rehearsal advice and readable resource handoff guidance. |
| `PROGRESS.md` | Saved this exact request, sources actually inspected, access failures/limits, observations, recommendations, and file-by-file changes. |

Checks: confirmed the cited URLs came from the participant channel or linked
source documents; matched suggested demo values to existing README/control
evidence; read back the changed guide and log. The revised timing spans 0:00–4:00
with all four views, CSV upload/export, process evidence and reflection. Application
code, data, tests, dependencies, and the native Google Doc were unchanged; no
application tests were rerun for these presentation-only documentation edits.

Next remains a rehearsal of the live demo, then recording and the remaining
required submission assets. Additional feature ideas remain for a later version.

## Streamline the submission package for instructors

Date: October 11, 2026 (America/Los_Angeles).

### Actual user prompt

```text
Ok so what are the changes that we should make to our submission package. Also, as I think about the work our instrucutors will have to do let's make sure they can easily access the information they could be looking for and are not drowned in information.
```

### Changes made and why

Reviewed the package from an instructor's perspective. The long README mixed
quick start and detailed usage; the Google Doc needed a clear review route and
submission-link labels. The goal was a short first review with optional evidence
available on demand.

Edited the same [Google Doc](https://docs.google.com/document/d/1TIGSyGoqxlsvoPzPaK28hKfmsxwxiNINdBWX9_7AUFc)
in its W1 Project folder. Page 1 now contains Start here, the marketer's purpose,
all four views/shared filters, documentation/video/code labels, a review route,
a shorter data/quality summary, baseline metrics, and verification scope. Pages
2–3 retain selected actual prompts, iteration details, checks and Hassan's expanded
reflection. Pages 4–9 are labelled Appendix A1–A6 so reviewers can find building
process, Overview, trends/metrics, platforms, campaign details and Time Series.
Normalized the metric table's backgrounds to a light header and white result rows
so no result gets accidental special emphasis.

The Doc and README explicitly mark video and GitHub links pending. Only the
existing documentation URL is linked; no placeholder link was presented as a
completed deliverable. The package checklist calls for direct links to all three
artifacts and signed-out access checks when those artifacts are ready.

### Every project file created or changed

| File | Actual change and purpose |
|---|---|
| `README.md` | Replaced the long entry page with about 355 words: purpose, three submission-link slots, evidence map, data/results/limits, and launch/test commands. Links detailed instructions and full history as optional evidence. |
| `docs/USER_GUIDE.md` | New optional guide preserving the previous README's detailed usage, view-by-view controls, edge cases, inspection procedure and chart notes. Added a return link to the concise README. |
| `SUBMISSION_GUIDE.md` | Added a reviewer-question/evidence-location table and final package order: record video, publish code, replace pending links, verify viewing access and submit. Recorded the Doc's main/appendix organization and kept rehearsal guidance. |
| `PROJECT_BRIEF.md` | Recorded the instructor-focused packaging milestone, concise README/optional guide, preserved evidence and remaining external assets. |
| `submission/document_manifest.json` | Updated the current native revision, modified timestamp and PDF hash. Recorded main/appendix pages, layout-check scope, preserved table/reflection, and pending video/repository links. Original local Word sources remain historical. |
| `PROGRESS.md` | Updated the current status and saved the exact request, native Doc changes, every file explanation, verification and remaining work. |

### Actual checks

- Read the native Doc's current revision and ranges before writing. Scoped edits
  used requiredRevisionId guards. Readback verified the expected headings, first
  page labels, exact documentation hyperlink, six image objects, six captions and
  one preserved native metric table. Hassan's expanded reflection matches the
  pre-edit text exactly.
- Exported the updated Google Doc to PDF and inspected all nine pages. The final
  first page was inspected after a last refinement listing all four views and
  applying consistent table shading. Rendered pages 2–9 of that final export were
  pixel-identical to the already-inspected pages. The document still has nine
  pages; the page 1 review route and README page references are correct.
- Final PDF SHA-256:
  b4fde346cd1d6b33b20491c964722b7c691e651d90204c1022d16a3e3790fd61.
- Native metadata confirms the same document ID, W1 Project parent, and owner-only
  access (shared=false). No public permission change or form submission occurred.
- Preserved the previous README body beginning at Use and verify the app in the
  new user guide; checked the concise README's local links and manifest JSON.
  No application code, tests, data, dependencies or screenshot files changed;
  application tests were not rerun for this documentation/navigation work.
- The Google Doc is the current submission document. Local DOCX files and their
  builder still preserve the initial draft. No second documentation deliverable
  was created.

Remaining work: rehearse and record the demo, place it on Drive, publish the code
to GitHub, fill both real links into the Doc and README, verify reviewer access,
then submit the three direct links through the form. The package is organized,
but those external deliverables and final access checks remain pending.

## Design content for a presenter-only demo guide

Date: October 11, 2026 (America/Los_Angeles). Status: **Content plan drafted; guide app not implemented.**

### Actual user request and audience choice

```text
I think a demo guide application would be very helpful. Let's design what the content of it should be.

[https://www.loom.com/share/dc56051ecf8f42568c290d534b459f19](https://www.loom.com/share/dc56051ecf8f42568c290d534b459f19)

This is an example I saw from one of the participants in the course
```

Asked an optional audience question:

```text
Who should the demo guide serve? I recommend two separate views so your speaking notes stay out of the instructors’ overview.
```

Hassan selected:

```text
Your presenter notes and rehearsal only
```

Revised the design to one presenter audience. No instructor-facing guide or extra
submission deliverable is planned. Earlier consideration of two audiences was
superseded by Hassan's explicit choice.

### Reference actually inspected

The web reader could not open the supplied Loom URL. Opened it in Chrome; title
was **SAT Prep App Demo, MVP Overview**, by Kavya, with player duration **3:55**.
Read the available transcript preview through about 2:42, the chapter labels,
and a paused frame around 1:12 showing a GitHub DEMO_GUIDE.md with workflow and
capability/benefit content. Dismissed optional sign-up prompts and paused muted
autoplay. The remaining transcript required sign-up; no account was created and
full video viewing was not claimed.

The visible frame supplied the actual
[demo guide URL](https://github.com/kavya3v/SAT_app/blob/main/docs/DEMO_GUIDE.md).
Fetched and read it through the GitHub connector. Useful content patterns:
opening pitch, MVP flow diagram, capability/show/benefit table, timed actions and
talking points, reference results, short architecture/technology explanation and
clear current/future scope. Used these patterns to organize our own verified
content; did not copy the peer's application features or run peer code.

### Files changed and reasons

| File | Actual change and purpose |
|---|---|
| `docs/DEMO_GUIDE_PLAN.md` | New draft content design for Hassan only. Includes preparation checklist, seven timed cue cards, exact actions, short narration, reference results, continue checkpoints, one worked card, expandable metric/architecture/evidence/recovery notes, and proposed manual navigation/timer controls. Labels the guide as unimplemented and traces facts to existing sources. |
| `SUBMISSION_GUIDE.md` | Added a pointer to the presenter-only content plan beside the rehearsal script; explicitly states it is a draft and adds no instructor deliverable. |
| `PROGRESS.md` | Saved this request, audience question/answer, reference-access scope, design choice, file explanations and checks. |

### Content decisions and checks

- The seven target windows preserve the approved 0:00–4:00 sequence and all four
  app views. Preparation is outside that timer; the final 45 seconds cover actual
  AI collaboration, one header bug/fix, recorded verification and learning.
- Cue cards separate actions, narration and expected results. Deep notes remain
  collapsed. Expected values are reference controls; guide navigation does not
  imply dashboard filters have changed or checks have automatically passed.
- Baseline: 4,040 records, 24 campaigns, USD 306,470.04 spend, 7,823 purchases.
  June/Instagram/Prospecting/Sales: 60 records, 2 campaigns, USD 9,394.52 spend,
  175 purchases. Full-window CMP010: 109 records, USD 20,971.68 spend, 500 purchases.
  Weekly full-window export: 27 periods. These match existing inspection/app-test
  evidence and the submission script.
- Explicitly explain scope changes: resetting dates before CMP010 restores the
  full window; Campaign Details' local search does not filter Time Series. The
  proposed download is a 27-period weekly table, not 4,040 daily campaign rows.
- Proposed controls: Previous/Next, step jump list, Start/Pause/Restart rehearsal
  timer, optional full notes/recovery, analyzer/Doc links and a final rehearsal
  review. Advance manually; guide notes stay outside the recorded area.
- Read back the new design and its guide link; checked the cue timings, primary
  counts/amounts and source references. No application code, tests, CSVs,
  dependencies, native Google Doc or compact README changed. Application tests
  were not rerun for this content-design task.

Next: review the proposed cue-card content with Hassan, then implement the small
presenter companion within the current project. No guide runtime, new dashboard
view, recording, deployment, sharing or form submission was created this turn.

## Recording supplied and Loom link selected

Date: October 11, 2026 (America/Los_Angeles). Status: **Recording link added to the submission package; video review and public access unverified.**

### Actual user prompts

```text
Ok here's the loom recording of the demo [https://www.loom.com/share/4aa51da9e63d4920a55c733ef40d2f22](https://www.loom.com/share/4aa51da9e63d4920a55c733ef40d2f22)
```

```text
It's ok to use the loom link
```

The previous attempt to review the recording failed: the web reader could not
open it, and computer-use tooling prohibited inspection of the recording URL.
That review stopped without file edits. The video was not watched and no duration,
content, or public-access result is claimed. Hassan then chose to use the Loom
link. This turn updated submission links only; it did not retry video inspection.
The earlier suggestion that a Drive copy was necessary is superseded by his choice.
The form's literal video field label remains documented as Video Demo Drive Link;
instructor acceptance of Loom has not been independently confirmed.

### Each file or document changed

| File/document | Actual change and reason |
|---|---|
| Existing native Google Doc | Replaced only the page-1 pending-video paragraph with a linked “watch on Loom” label, using a revision-guarded native edit. Gives instructors direct access to Hassan's chosen recording. |
| README.md | Replaced the pending-video row with the same direct Loom link. |
| SUBMISSION_GUIDE.md | Marked the recording as supplied, removed Drive upload as a planned step, preserved the form's exact field label, and listed the remaining duration/access, GitHub and submission checks. Kept rehearsal notes as optional reference and corrected the detailed-guide reference. |
| PROJECT_BRIEF.md | Updated the current submission milestone and next step to reflect the recording link and pending GitHub publication. |
| PROGRESS.md | Updated the current status and recorded the actual prompts, link choice, inspection limitation, file changes and checks. Historical milestone entries remain as the build record. |
| submission/document_manifest.json | Saved the video URL, unverified duration/content/access status, current native revision and modification timestamp, PDF hash, and scoped link/layout checks. |

### Checks actually completed

- Read back the native video paragraph and its hyperlink; the target exactly
  matches Hassan's Loom URL. His expanded reflection is unchanged verbatim.
  All six embedded images and the native metric table remain present.
- Exported the updated Google Doc to a temporary PDF. It remains nine pages;
  visually inspected the revised page 1 and its readable link/table layout.
  Other pages were not visually reinspected this turn.
- The Doc's sharing metadata still reports owner-only access. No permission
  changes, repository publication, or form submission occurred.
- Checked the local links/status text and manifest JSON. App code, tests, data,
  dependencies and port 8502 are unchanged. Application tests were not rerun
  for these documentation edits; the latest application run passed 45 tests.

Next: publish the code to GitHub as a separate step, add its direct link, then
confirm the recording is at most five minutes and verify reviewer access to
all three artifacts before submitting the Google Form. The presenter-guide
application remains an unimplemented optional plan; it is not a submission blocker.
