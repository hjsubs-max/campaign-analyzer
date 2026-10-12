# Ad Campaign Performance Analyzer

Hassan's Maven Week 1 **Path B** project. A marketer can load one CSV, compare
channels, inspect campaigns, and follow performance over time. Built with
Python, Streamlit, pandas, and Plotly, with Codex assisting development and testing.

## Submission links

| Deliverable | Open |
|---|---|
| Project documentation | [Google Doc — start on page 1](https://docs.google.com/document/d/1TIGSyGoqxlsvoPzPaK28hKfmsxwxiNINdBWX9_7AUFc) |
| Demo video | [Watch demo on Loom](https://www.loom.com/share/4aa51da9e63d4920a55c733ef40d2f22) |
| Source code | [GitHub repository](https://github.com/hjsubs-max/campaign-analyzer) |

## Where to find the evidence

- **Doc pages 1–3:** project/data summary, selected actual prompts, iterations,
  verification, and Hassan's personal reflection.
- **Doc pages 4–9:** optional screenshot and metric-detail appendices, labelled
  A1–A6 in the document outline.
- **Detailed usage:** [user guide](docs/USER_GUIDE.md).
- **Full prompt/change/check history:** [build log](PROGRESS.md), optional supporting evidence.

## Dataset and verified results

The included `campaign_data_synthetic.csv` is clearly labelled synthetic:
**4,040 campaign-day records**, **24 campaigns**, April 1–September 30, 2026.
Each row is one campaign on one reporting date. Money is USD; conversions mean
attributed purchases.

With filters reset: **USD 306,470.04 spend**, **USD 839,690.13 attributed revenue**,
**7,823 purchases**, **1.45% CTR**, **USD 39.18 CPA**, and **2.74× ROAS**.
The latest application suite passed **45 tests**, covering validation, aggregate
rates, shared filters, search, and missing/zero inputs.

All four views—Overview, Platform Comparison, Campaign Details, and Time Series—
share date, channel, audience, and campaign-goal filters. Ratios use summed inputs.
Missing revenue and dates remain unknown; zero denominators display N/A.
ROAS describes attributed revenue relative to ad spend, not business profit or
causal advertising lift.

## Run locally

Open the folder containing `app.py`. From the VS Code `Project` workspace,
first run `cd campaign-analyzer`, then:

```sh
uv sync --locked
uv run --locked python -B -m streamlit run app.py --server.address=127.0.0.1 --server.port=8502 --browser.gatherUsageStats=false
```

Open **http://127.0.0.1:8502**. The synthetic demo loads automatically;
no model API key is needed. If it is already running, use the existing page.
Stop with Ctrl+C. On VS Code, select `campaign-analyzer/.venv/bin/python`.

To reproduce the checks:

```sh
uv run --locked python -B -m unittest discover -s tests -v
```

Optional references: [dataset guide](campaign_dataset_guide.txt),
[independent inspection controls](DATA_INSPECTION.json),
[project brief](PROJECT_BRIEF.md), and [detailed user guide](docs/USER_GUIDE.md).
