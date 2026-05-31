from __future__ import annotations

import altair as alt
import pandas as pd


def line_chart(frame, metric: str, title: str):
    return (
        alt.Chart(frame)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y(f"{metric}:Q", title=title),
            tooltip=["date:T", alt.Tooltip(f"{metric}:Q", title=title)],
        )
        .properties(title=title, width="container")
    )


def benchmark_chart(observed: float, target: float, metric_label: str):
    chart_frame = pd.DataFrame(
        {"category": ["Observed", "Target"], "value": [observed, target]}
    )
    return (
        alt.Chart(chart_frame)
        .mark_bar()
        .encode(
            x=alt.X("category:N", title=""),
            y=alt.Y("value:Q", title=metric_label),
            color=alt.Color("category:N", legend=None),
        )
        .properties(title=metric_label, width="container")
    )


def activity_minutes_chart(frame):
    return (
        alt.Chart(frame)
        .mark_bar()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("minutes:Q", title="Minutes"),
            color=alt.Color("activity:N", title="Activity"),
            tooltip=["date:T", "activity:N", alt.Tooltip("minutes:Q", title="Minutes")],
        )
        .properties(title="Minutes Spent Each Day by Activity", width="container")
    )
