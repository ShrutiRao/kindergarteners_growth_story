from __future__ import annotations

import pandas as pd
import streamlit as st

from services.datagov import dataset_metadata
from src.analytics import latest_observation, summarize_progress
from src.charts import line_chart


def render_public_context():
    meta = dataset_metadata()
    st.caption(f"Public context source: {meta['title']}")
    st.link_button("Open Data.gov source", meta["landing_page"])


def render_history_tab(frame: pd.DataFrame | None = None):
    st.header("Historical Snapshot")
    render_public_context()

    frame = frame if frame is not None else st.session_state.get("growth_frame")
    if frame is None or getattr(frame, "empty", True):
        st.info("Add or upload observations in the Input tab to see trends here.")
        return

    latest = latest_observation(frame)
    summary = summarize_progress(frame, "reading_minutes")
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest reading minutes", latest["reading_minutes"])
    col2.metric("First reading minutes", summary["start"])
    col3.metric("Change", summary["delta"])
    st.altair_chart(line_chart(frame, "reading_minutes", "Reading Minutes Over Time"), use_container_width=True)
