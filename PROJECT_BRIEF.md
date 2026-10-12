# Project brief

**Owner:** Hassan  
**Course:** Maven, Mastering Agentic AI, Week 1  
**Assignment:** Ad Campaign Performance Analyzer, Path B  
**Workspace:** `Project`  
**Project folder:** `Project/campaign-analyzer`, alongside `Mastering-Agentic-AI-Week1`  
**Working demo dataset:** Hassan supplied `campaign_data_synthetic.csv` (4,040
synthetic rows, 24 campaigns, April 1–September 30, 2026). Dataset inspection is
complete; CSV loading, validation, all four views, and shared filters are implemented.
The supplied guide defines all
conversions as attributed purchases and all money as USD. A header-compatible
copy is available as `campaign_data_synthetic_compatible.csv`; the uploader
accepts either header convention. Stock data is separate.

## Purpose and working style

Build an ad campaign analyzer while learning AI-assisted coding. Explain each step
in plain language. On every turn, explain each file changed, what changed, and why,
so Hassan can follow along and ask questions. Keep progress and verification evidence suitable for the course
submission. Work in stages, completing setup before implementing the full dashboard.

## Technology

- Python, with an isolated environment managed by uv.
- Streamlit for the app and interactive controls.
- pandas for data loading, filtering, and aggregation.
- Plotly for interactive charts.

## Finished app requirements

1. **Overview:** show campaign performance at a glance.
2. **Platform Comparison:** compare advertising channels.
3. **Campaign Details:** provide a searchable campaign table.
4. **Time Series:** show results over time.

All views must apply the same date, channel, audience, and campaign-goal filters.
Calculate metrics from aggregated totals rather than averaging row-level rates.
Handle missing data explicitly; do not silently convert unknown values into zero
activity. Ratios with a zero denominator should be shown as unavailable, not as
infinity or a misleading zero. Define the row meaning and supported metrics after
a dataset is selected and inspected.

## Completed milestone: setup

- Inspect the workspace and check Python, uv, and Git.
- Create a separate project folder alongside the course repo.
- Set up an isolated Python environment using uv and install required packages.
- Create and run a minimal Streamlit starter page.
- Save this brief as `PROJECT_BRIEF.md` and record actual progress in `PROGRESS.md`.
- Report what worked, blockers, and the exact launch command.

This milestone stopped at a minimal starter; dataset inspection followed separately.
Earlier stock-portfolio work remains separate.
`campaign-analyzer` is the project folder. No API key is needed for the app.

## Completed milestone: dataset inspection

One row is one campaign's results on one reporting date. Campaign ID fixes its
channel, audience, and goal. The saved CSV passes structural checks, reference
totals, and zero-denominator examples; there are no gaps inside documented active
windows. `inspect_dataset.py`, `DATA_INSPECTION.json`, and
`dataset_inspection.ipynb` preserve reproducible checks.

## Completed milestone: CSV loader

The original CSV is the default demonstration source, with a visible synthetic
label. The uploader normalizes `campaign_goal` → `goal` and `data_source` →
`dataset_type` so both supplied CSVs work. It validates daily campaign records,
shows a bounded preview, and exports validated data. Required malformed or missing
values are rejected; missing revenue is accepted as unknown with a warning.

## Completed milestone: Overview and shared filters

Date, channel, audience, and campaign-goal filters now feed one common filtered
DataFrame. Overview shows six summary cards, a spend-by-channel chart, metric
details, a bounded daily-record table, and a filtered download. Reset restores
visible selections and results. Empty selections and invalid date ranges are clear.
The app remains on port 8502.

## Completed milestone: Platform Comparison and Campaign Details

The sidebar switches between Overview, Platform Comparison, and Campaign Details.
Platform Comparison has a selectable metric chart and channel-level aggregate table.
Campaign Details has literal, case-insensitive campaign search, an aggregate summary,
a campaign selector, and selected-campaign daily records. Local search/selection
cannot bypass global filters. `views.py` shares display functions; all calculations
continue to use `analysis.py` and the same filtered DataFrame.

## Completed milestone: Time Series

Daily and Monday–Sunday weekly trends support selectable metrics, an interactive
chart, a period table, and CSV export. Each period's ratios use its aggregated
totals. Dates with no records remain unknown; chart lines do not bridge missing
values. Weekly boundaries are clipped to the selected dates and partial weeks are
labelled. Coverage counts dates with at least one selected record, not proof of
complete campaign reporting. All four views share the same filters and definitions.

## Completed milestone: browser checks and submission guide

Verified the real upload picker, actual daily/Overview downloads, and grouped export
payloads. A 900-pixel responsive preview revealed metric-card clipping; narrow
metric rows now wrap so complete values remain visible. SUBMISSION_GUIDE.md
contains a four-minute walkthrough and screenshot checklist. PROGRESS.md records
the actual checks and their scope. Physical mobile devices were not tested.

## Official submission requirements verified October 11, 2026

The Week 1 handout requires a Google Doc containing overview, dataset, actual
prompts, iterations, learning observations, and process screenshots; a live demo
video of five minutes or less; and code assets on GitHub. The Google Form asks for
GitHub, video Drive, and documentation Drive links, plus name/email. All links
must be publicly accessible. Submit using Google Forms, not Maven's editor.
Maven lists Sunday, October 11, 2026, 11:59 p.m. Pacific as the deadline for Builder
of the Week consideration. Late submission remains allowed without award
consideration; the project is not required for the certificate. Source links and
the exact checklist are in SUBMISSION_GUIDE.md. Nothing has been publicly shared
or submitted.

## Completed follow-up: Overview spend-versus-conversions trend

Overview now includes aligned daily spend and conversion panels below the channel
chart. Dates are shared, units are separate, totals use all selected records, and
missing dates remain gaps. The trend reconciles to baseline and filtered controls.

## Completed submission milestone: Google Doc draft

The [project documentation Google Doc](https://docs.google.com/document/d/1TIGSyGoqxlsvoPzPaK28hKfmsxwxiNINdBWX9_7AUFc)
is now in Hassan's
[W1 Project folder](https://drive.google.com/drive/folders/1p5_XTZxWlf2HQbzzDO2PV48nu9e9XStF),
after he moved the same file and expanded his reflection. Its link is unchanged.
It includes project/data context, selected actual prompts, bugs and iterations,
verification scope, six genuine process/app screenshots, and Hassan's reflection.
All nine pages were inspected when the draft was created. After Hassan's edit,
native readback confirmed the expanded reflection and six images; the revised
reflection and following page were visually checked, and the PDF remains nine
pages. It remains private to its owner.

The instructor-focused packaging pass adds a one-page Start here summary and
submission-link labels to the same Doc. Pages 1–3 cover the main project/process/
reflection narrative; pages 4–9 are clearly labelled A1–A6 evidence appendices.
The concise README provides the same navigation and launch/check commands;
`docs/USER_GUIDE.md` preserves detailed instructions as optional supporting material.
Hassan's expanded reflection, original prompts, metric table, and six screenshots
remain intact. Final layout and page references were verified. The Loom video
and GitHub links are now present. The public repository is
[hjsubs-max/campaign-analyzer](https://github.com/hjsubs-max/campaign-analyzer).
No Google Doc sharing changes or form submission have been performed.

Hassan supplied his recording and explicitly chose to use the Loom link. Its
duration, contents, and reviewer viewing access remain unverified. Hassan
requested one step at a time: GitHub publication is complete; final duration/access
checks and form submission are next. Original document source and evidence are in
`submission/`; the Google Doc is the current version with Hassan's edits. These
documentation milestones changed no app code, source data, or dependencies.

## Completed milestone: public GitHub repository

Published 22 project files: app modules, tests, primary and compatible synthetic
CSVs, dependency files, dataset/inspection evidence, README, user guide, brief and
build log. Local submission-generation files and preparation notes remain outside
Git. The repository's file bytes reconciled with the local project; an unauthenticated
clone passed all 45 tests using the existing isolated Python environment. This
checks the submitted code without claiming a fresh dependency installation.
Git is initialized only inside campaign-analyzer and tracks origin/main. App code,
CSV contents, dependency versions and port 8502 are unchanged.

Use aggregated numerators and denominators for all ratios. Treat zero denominators
as N/A and genuine zero numerators as zero. Do not fill unknown revenue with zero;
revenue-dependent metrics must be unavailable when selected inputs are incomplete.
Reject invalid essential fields with a clear explanation rather than dropping
records. Missing dates must stay distinguishable from recorded zero activity.
