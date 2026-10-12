"""Display all four views using common aggregate metric definitions."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from analysis import aggregate_campaigns, aggregate_time_series, summarize

# Name, shared calculation key, visible unit label, formatted value.
COMPARISON_METRICS = {
    "Spend": ("spend", "Spend", "{:,.2f}"),
    "Attributed revenue": ("revenue", "Attributed revenue", "{:,.2f}"),
    "Purchases": ("conversions", "Purchases", "{:,.0f}"),
    "CTR": ("ctr_pct", "CTR (%)", "{:.2f}%"),
    "Purchase conversion rate": ("cvr_pct", "Purchase conversion rate (%)", "{:.2f}%"),
    "CPC": ("cpc", "CPC", "{:,.2f}"),
    "CPA": ("cpa", "CPA", "{:,.2f}"),
    "CPM": ("cpm", "CPM", "{:,.2f}"),
    "ROAS": ("roas", "ROAS (×)", "{:.2f}×"),
    "Ad-spend return": ("ad_spend_return_pct", "Ad-spend return (%)", "{:.2f}%"),
}
CAMPAIGN_DIMENSIONS = ["campaign_id", "campaign_name", "channel", "audience", "goal"]
TABLE_MEASURES = ["impressions", "clicks", "conversions", "spend", "revenue",
                  "ctr_pct", "cvr_pct", "cpc", "cpa", "cpm", "roas", "missing_revenue_rows"]
TREND_METRICS = {**COMPARISON_METRICS,
                 "Impressions": ("impressions", "Impressions", "{:,.0f}"),
                 "Clicks": ("clicks", "Clicks", "{:,.0f}")}


def format_metric(value, pattern):
    return "N/A" if value is None or pd.isna(value) else pattern.format(value)


def render_cards(data, currency, scope="shared filters"):
    metrics = summarize(data)
    if metrics["missing_revenue_rows"]:
        st.warning(f"Revenue is missing in {metrics['missing_revenue_rows']:,} of {len(data):,} selected rows. Revenue, ROAS, ad-spend return, and revenue per purchase are N/A; unknown revenue is not zero.")
    for cards in [
        [(f"Spend ({currency})", "spend", "{:,.2f}", "Total advertising spend in the selected rows."),
         (f"Attributed revenue ({currency})", "revenue", "{:,.2f}", "Total attributed revenue; unavailable if any selected revenue is unknown."),
         ("Purchases", "conversions", "{:,.0f}", "Sum of conversions. All conversions in the demo are attributed purchases.")],
        [("CTR", "ctr_pct", "{:.2f}%", "Total clicks ÷ total impressions × 100."),
         (f"CPA ({currency})", "cpa", "{:,.2f}", "Total spend ÷ total purchases. This is cost per purchase, not new-customer acquisition cost."),
         ("ROAS", "roas", "{:.2f}×", "Total attributed revenue ÷ total spend; not profit.")],
    ]:
        for column, (label, key, pattern, help_text) in zip(st.columns(3), cards):
            column.metric(label, format_metric(metrics[key], pattern), help=help_text)
    st.caption(f"Cards use all {len(data):,} records within {scope}, including rows outside the table preview. N/A means a zero denominator or incomplete inputs.")


def render_channel_chart(grouped, metric_name, currency, context):
    field, label, pattern = COMPARISON_METRICS[metric_name]
    if field in {"spend", "revenue", "cpc", "cpa", "cpm"}:
        label = f"{label} ({currency})"
    st.subheader(f"{metric_name} by channel")
    st.caption(f"{currency} · {context}")
    available = grouped.loc[grouped[field].notna()].sort_values(field).copy()
    excluded = len(grouped) - len(available)
    if excluded:
        noun, verb = ("channel", "has") if excluded == 1 else ("channels", "have")
        st.info(f"{excluded} {noun} {verb} unavailable {metric_name} and cannot be plotted. All channels remain in the comparison table with blank N/A values where needed.")
    if available.empty:
        st.info("This metric is unavailable for every selected channel. Choose another comparison metric.")
        return
    available["spend_hover"] = available.spend.map(lambda v: format_metric(v, "{:,.2f}"))
    available["revenue_hover"] = available.revenue.map(lambda v: format_metric(v, "{:,.2f}"))
    available["metric_label"] = available[field].map(lambda v: format_metric(v, pattern))
    figure = px.bar(available, x=field, y="channel", orientation="h", text="metric_label",
        labels={field: label, "channel": "Channel"},
        custom_data=["impressions", "clicks", "conversions", "spend_hover", "revenue_hover", "missing_revenue_rows", "metric_label"],
        color_discrete_sequence=["#357ABD"], template="plotly_white")
    figure.update_traces(texttemplate="%{text}", textposition="auto",
        hovertemplate="%{y}<br>Selected metric: %{customdata[6]}<br>Impressions: %{customdata[0]:,.0f}<br>Clicks: %{customdata[1]:,.0f}<br>Purchases: %{customdata[2]:,.0f}<br>Spend: %{customdata[3]}<br>Revenue: %{customdata[4]}<br>Unknown revenue rows: %{customdata[5]:,.0f}<extra></extra>")
    figure.update_xaxes(range=[min(float(available[field].min()) * 1.12, 0),
                              max(float(available[field].max()) * 1.12, 1)], zeroline=True)
    figure.update_layout(height=340, margin=dict(l=10, r=30, t=10, b=10), showlegend=False)
    st.plotly_chart(figure, width="stretch")


def numeric_column_config(currency):
    config = {
        "impressions": st.column_config.NumberColumn("Impressions", format="%d"),
        "clicks": st.column_config.NumberColumn("Clicks", format="%d"),
        "conversions": st.column_config.NumberColumn("Purchases", format="%d"),
        "ctr_pct": st.column_config.NumberColumn("CTR (%)", format="%.2f"),
        "cvr_pct": st.column_config.NumberColumn("Purchase CVR (%)", format="%.2f"),
        "roas": st.column_config.NumberColumn("ROAS (×)", format="%.2f"),
        "missing_revenue_rows": st.column_config.NumberColumn("Unknown revenue rows", format="%d"),
    }
    for key in ["spend", "revenue", "cpc", "cpa", "cpm"]:
        config[key] = st.column_config.NumberColumn(f"{key.upper() if len(key) == 3 else key.title()} ({currency})", format="%.2f")
    return config


def render_daily_records(data, currency, filename="campaign_data_filtered.csv"):
    st.subheader("Filtered daily records")
    st.caption("One row represents one campaign on one reporting date. The demo's conversions are attributed purchases.")
    preview_size = st.selectbox("Preview rows", [10, 50, 100, 500], index=1, key="daily_preview_rows")
    display = data.head(preview_size).copy()
    display["date"] = display.date.dt.strftime("%Y-%m-%d")
    st.dataframe(display, hide_index=True, width="stretch", column_config=numeric_column_config(currency))
    st.caption(f"Showing {len(display):,} of {len(data):,} selected rows. Missing revenue remains blank in the preview.")
    export = data.copy()
    export["date"] = export.date.dt.strftime("%Y-%m-%d")
    st.download_button("Download filtered CSV", data=export.to_csv(index=False).encode("utf-8"),
        file_name=filename, mime="text/csv")


def render_metric_details(data, currency):
    metrics = summarize(data)
    with st.expander("Metric details and definitions"):
        details = [
            ("Impressions", "impressions", "{:,.0f}", "Sum of impressions"),
            ("Clicks", "clicks", "{:,.0f}", "Sum of clicks"),
            ("Purchase conversion rate", "cvr_pct", "{:.2f}%", "Purchases / clicks × 100"),
            (f"CPC ({currency})", "cpc", "{:,.2f}", "Spend / clicks"),
            (f"CPM ({currency})", "cpm", "{:,.2f}", "Spend / impressions × 1,000"),
            ("Ad-spend return", "ad_spend_return_pct", "{:.2f}%", "(Revenue − spend) / spend × 100"),
            (f"Revenue per purchase ({currency})", "revenue_per_purchase", "{:,.2f}", "Revenue / purchases"),
        ]
        st.dataframe([{"Metric": label, "Value": format_metric(metrics[key], pattern), "Formula": formula}
                      for label, key, pattern, formula in details], hide_index=True, width="stretch")
        st.caption("All ratios use summed numerators and denominators. Ad-spend return excludes product and operating costs, so it is not full business profit ROI.")


def render_overview_trends(data, currency, context, start, end):
    daily = aggregate_time_series(data, start, end)
    st.subheader("Spend and conversions over time")
    st.caption(f"Daily totals · {currency} · {context} · Channels: {', '.join(sorted(data.channel.unique()))}")
    st.caption("Aligned panels share dates and have separate units. Conversions are attributed purchases in the demo. The patterns do not establish that spend caused purchases.")
    missing = int(daily.unrecorded_days.sum())
    if missing:
        st.info(f"{missing:,} calendar dates have no selected records. Both panels leave those dates as gaps; recorded zero activity stays zero.")
    figure = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.12,
                           subplot_titles=[f"Spend ({currency})", "Conversions (purchases)"])
    for row, field, label, pattern, dash, symbol in [
        (1, "spend", f"Spend ({currency})", "{:,.2f}", "solid", "circle"),
        (2, "conversions", "Conversions (purchases)", "{:,.0f}", "dash", "diamond"),
    ]:
        hover = list(zip(daily[field].map(lambda value: format_metric(value, pattern)), daily.recorded_rows))
        figure.add_trace(go.Scatter(x=daily.period_start, y=daily[field], name=label,
            mode="lines+markers", connectgaps=False, line=dict(color="#357ABD", width=2, dash=dash),
            marker=dict(size=4, symbol=symbol), customdata=hover,
            hovertemplate=f"Date: %{{x|%Y-%m-%d}}<br>{label}: %{{customdata[0]}}<br>Campaign-day records: %{{customdata[1]}}<extra></extra>"), row=row, col=1)
        figure.update_yaxes(title_text=label, rangemode="tozero", zeroline=True, row=row, col=1)
    figure.update_xaxes(type="date")
    figure.update_xaxes(title_text="Reporting date", row=2, col=1)
    figure.update_layout(template="plotly_white", height=520, showlegend=False,
                         margin=dict(l=10, r=20, t=35, b=10))
    st.plotly_chart(figure, width="stretch")


def render_overview(data, currency, context, start, end):
    render_cards(data, currency)
    render_channel_chart(aggregate_campaigns(data, ["channel"]), "Spend", currency, context)
    render_overview_trends(data, currency, context, start, end)
    render_daily_records(data, currency)
    render_metric_details(data, currency)


def render_platform_comparison(data, currency, context):
    render_cards(data, currency)
    metric = st.selectbox("Compare metric", list(COMPARISON_METRICS), key="platform_metric")
    grouped = aggregate_campaigns(data, ["channel"])
    render_channel_chart(grouped, metric, currency, context)
    st.subheader("Channel comparison")
    st.caption("One row per selected channel. Ratios use each channel's totals. Blank metric cells mean N/A, not zero.")
    st.dataframe(grouped[["channel", *TABLE_MEASURES]], hide_index=True, width="stretch",
                 column_config=numeric_column_config(currency))
    st.download_button("Download channel comparison", grouped.to_csv(index=False).encode("utf-8"),
                       file_name="channel_comparison.csv", mime="text/csv")
    render_metric_details(data, currency)


def render_campaign_details(data, currency, source_key):
    query = st.text_input("Search campaigns", key=f"campaign_search_{source_key}",
                         help="Literal, case-insensitive search across campaign ID, name, channel, audience, and goal.").strip()
    campaigns = aggregate_campaigns(data, CAMPAIGN_DIMENSIONS)
    if query:
        mask = campaigns[CAMPAIGN_DIMENSIONS].apply(
            lambda col: col.astype(str).str.contains(query, case=False, regex=False, na=False)
        ).any(axis=1)
        campaigns = campaigns.loc[mask].copy()
    if campaigns.empty:
        st.info("No campaigns match this search within the shared filters. Clear the search or adjust the filters.")
        return
    st.subheader("Searchable campaign summary")
    noun = "campaign" if len(campaigns) == 1 else "campaigns"
    st.caption(f"{len(campaigns):,} matching {noun} within the shared filters. One aggregate row per campaign; blank metric cells mean N/A.")
    st.dataframe(campaigns[[*CAMPAIGN_DIMENSIONS, *TABLE_MEASURES]], hide_index=True, width="stretch",
                 column_config={**numeric_column_config(currency),
                                "campaign_name": st.column_config.TextColumn("Campaign name", width="medium")})
    st.download_button("Download matching campaigns", campaigns.to_csv(index=False).encode("utf-8"),
                       file_name="matching_campaigns.csv", mime="text/csv")

    ids = list(campaigns.campaign_id)
    labels = dict(zip(campaigns.campaign_id, campaigns.campaign_name))
    selected_key = f"campaign_pick_{source_key}"
    if st.session_state.get(selected_key) not in ids:
        st.session_state[selected_key] = ids[0]
    selected_id = st.selectbox("Campaign", ids, index=None, key=selected_key,
                              format_func=lambda cid: f"{labels[cid]} ({cid})")
    selected = data.loc[data.campaign_id.eq(selected_id)].copy()
    st.subheader(f"Selected campaign: {labels[selected_id]} ({selected_id})")
    metadata = selected.iloc[0]
    st.caption(f"{metadata.channel} · {metadata.audience} · {metadata.goal} · "
               f"{len(selected):,} daily records within the shared filters")
    render_cards(selected, currency, scope="the selected campaign and shared filters")
    render_daily_records(selected, currency, filename="selected_campaign_records.csv")
    render_metric_details(selected, currency)
    st.caption("Search and Campaign selection affect this view only. The shared Reset button resets date/channel/audience/goal filters; clear Search campaigns separately.")


def render_time_series(data, currency, context, start, end):
    render_cards(data, currency)
    controls = st.columns(2)
    frequency = controls[0].selectbox("Time interval", ["Daily", "Weekly"], key="trend_interval")
    metric = controls[1].selectbox("Trend metric", list(TREND_METRICS), key="trend_metric")
    periods = aggregate_time_series(data, start, end, frequency)
    field, label, pattern = TREND_METRICS[metric]
    if field in {"spend", "revenue", "cpc", "cpa", "cpm"}:
        label = f"{label} ({currency})"
    st.subheader(f"{metric} over time")
    st.caption(f"{frequency} · {currency} · {context} · Channels: {', '.join(sorted(data.channel.unique()))}")
    st.caption("Each point uses that period's recorded totals; rates are never averaged across days. Weekly periods run Monday–Sunday and are clipped at the selected date boundaries.")
    missing_days = int(periods.unrecorded_days.sum())
    if missing_days:
        dates_text = "date has" if missing_days == 1 else "dates have"
        st.info(f"{missing_days:,} selected calendar {dates_text} no records. Activity on those dates is unknown, not zero. Weekly totals include only recorded days; inspect coverage before comparing periods.")
    st.caption("Days with records means at least one selected campaign reported that day; it does not prove every campaign reported. Partial week means the date filters include fewer than seven days of that week.")

    unavailable = int(periods[field].isna().sum())
    if unavailable:
        st.info(f"{unavailable:,} periods have unavailable {metric}. Blank table values mean N/A; line gaps preserve missing data or undefined ratios.")
    if periods[field].notna().any():
        plot = periods.copy()
        plot["metric_label"] = plot[field].map(lambda value: format_metric(value, pattern))
        figure = px.line(plot, x="period_start", y=field, markers=True,
            labels={"period_start": "Reporting period start", field: label},
            custom_data=["period_end", "recorded_days", "window_days", "recorded_rows",
                         "coverage", "partial_week", "metric_label"],
            color_discrete_sequence=["#357ABD"], template="plotly_white")
        figure.update_traces(connectgaps=False,
            hovertemplate="Start: %{x|%Y-%m-%d}<br>End: %{customdata[0]|%Y-%m-%d}<br>Selected metric: %{customdata[6]}<br>Days with records: %{customdata[1]} / %{customdata[2]}<br>Campaign-day records: %{customdata[3]}<br>%{customdata[4]}<br>Partial week: %{customdata[5]}<extra></extra>")
        figure.update_xaxes(type="date")
        figure.update_yaxes(rangemode="tozero", zeroline=True)
        figure.update_layout(height=380, margin=dict(l=10, r=20, t=10, b=10), showlegend=False)
        st.plotly_chart(figure, width="stretch")
    else:
        st.info("This metric is unavailable for every selected period. Choose another trend metric.")

    st.subheader("Period totals and coverage")
    table = periods.copy()
    for column in ["period_start", "period_end"]:
        table[column] = table[column].dt.strftime("%Y-%m-%d")
    columns = ["period_start", "period_end", "recorded_days", "window_days", "unrecorded_days",
               "recorded_rows", "partial_week", "coverage", *TABLE_MEASURES, "ad_spend_return_pct"]
    st.dataframe(table[columns], hide_index=True, width="stretch", column_config={
        **numeric_column_config(currency),
        "recorded_days": st.column_config.NumberColumn("Days with records", format="%d"),
        "window_days": st.column_config.NumberColumn("Days in selected window", format="%d"),
        "unrecorded_days": st.column_config.NumberColumn("Days without records", format="%d"),
        "recorded_rows": st.column_config.NumberColumn("Campaign-day records", format="%d"),
        "partial_week": st.column_config.CheckboxColumn("Partial week"),
        "ad_spend_return_pct": st.column_config.NumberColumn("Ad-spend return (%)", format="%.2f"),
    })
    st.caption("Blank metrics mean N/A. Period totals cover observed records only. Do not sum partial known revenue into a complete total or average period rates into an overall rate.")
    st.download_button("Download time series", table.to_csv(index=False).encode("utf-8"),
                       file_name=f"campaign_time_series_{frequency.lower()}.csv", mime="text/csv")
    render_metric_details(data, currency)
