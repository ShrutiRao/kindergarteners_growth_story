from __future__ import annotations

import pandas as pd
import streamlit as st

from src.analytics import summarize_progress
from src.benchmarks import benchmark_overview, compare_to_standard
from src.charts import benchmark_chart


def render_comparison_tab(standards: pd.DataFrame, frame: pd.DataFrame | None = None, child_profile: dict | None = None):
    st.header("Comparison")
    st.caption("Metric cards below compare the latest observation against local age and grade expectations.")

    frame = frame if frame is not None else st.session_state.get("growth_frame")
    child_profile = child_profile or st.session_state.get("child_profile") or {"sex": "boy", "age_years": 5}

    if frame is None or getattr(frame, "empty", True):
        st.info("Add or upload observations in the Input tab to see benchmark comparisons.")
        return

    latest = frame.sort_values("date").iloc[-1]
    overview = benchmark_overview(frame=frame, child_profile=child_profile, standards=standards)
    if not overview:
        st.warning("No benchmark matches were found for the current child profile and standards table.")
        return
    metric_columns = st.columns(len(overview))
    for column, item in zip(metric_columns, overview, strict=False):
        delta_value = item["gap_to_target"]
        delta_label = None if delta_value is None else f"{delta_value:+.0f}"
        column.metric(item["metric"].replace("_", " ").title(), item["value"], delta=delta_label)
        column.caption(f"Target: {item['expected_target']} {item['unit']}")

    age_months = int(child_profile["age_years"]) * 12
    result = compare_to_standard(
        metric="reading_minutes",
        value=float(latest["reading_minutes"]),
        age_months=age_months,
        sex=child_profile["sex"],
        standards=standards,
    )

    progress = summarize_progress(frame, "reading_minutes")
    progress_col1, progress_col2 = st.columns(2)
    progress_col1.metric("Reading trend start", progress["start"])
    progress_col2.metric("Reading trend change", progress["delta"])

    if result.get("expected_target") is not None:
        st.altair_chart(
            benchmark_chart(
                observed=float(latest["reading_minutes"]),
                target=float(result["expected_target"]),
                metric_label="Reading Minutes",
            ),
            use_container_width=True,
        )
