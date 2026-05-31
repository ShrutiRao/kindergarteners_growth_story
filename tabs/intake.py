from __future__ import annotations

import pandas as pd
import streamlit as st

from src.io import (
    growth_frame_from_manual_entry,
    growth_template_frame,
    normalize_growth_frame,
)
from src.validation import validate_child_profile, validate_growth_frame


def render_intake_tab():
    st.header("Input")
    st.caption("Upload a CSV or enter the latest observation manually. The same child profile is used throughout the dashboard.")

    child_name = st.text_input("Child name")
    sex = st.selectbox("Sex", ["boy", "girl"])
    age_years = st.number_input("Age in years", min_value=0, max_value=20, value=5)
    grade_level = st.text_input("Grade level", value="Kindergarten")

    st.session_state["child_profile"] = {
        "child_name": child_name,
        "sex": sex,
        "age_years": int(age_years),
        "grade_level": grade_level,
    }

    upload = st.file_uploader("Upload growth CSV", type=["csv"])
    if upload is not None:
        frame = pd.read_csv(upload)
        normalized = normalize_growth_frame(frame)
        validate_growth_frame(normalized)
        st.session_state["growth_frame"] = normalized
        st.success("CSV loaded.")
        st.dataframe(normalized)

    template_frame = growth_template_frame()
    st.download_button(
        label="Download CSV template",
        data=template_frame.to_csv(index=False).encode("utf-8"),
        file_name="kindergarten_growth_metrics_template.csv",
        mime="text/csv",
    )

    st.subheader("Manual entry")
    manual_entry = {
        "Date": st.date_input("Observation date"),
        "Reading_Minutes": st.number_input("Reading minutes", min_value=0, value=20),
        "Books_Read": st.number_input("Books read", min_value=0, value=1),
        "Sight_Words_Mastered": st.number_input("Sight words mastered", min_value=0, value=5),
        "Letters_Recognized": st.number_input("Letters recognized", min_value=0, value=26),
        "Writing_Score": st.number_input("Writing score", min_value=0, value=3),
        "Math_Problems_Correct": st.number_input("Math problems correct", min_value=0, value=8),
        "Screen_Time_Minutes": st.number_input("Screen time minutes", min_value=0, value=30),
        "Outdoor_Play_Minutes": st.number_input("Outdoor play minutes", min_value=0, value=60),
        "Mood": st.text_input("Mood", value="Happy"),
        "Teacher_Feedback": st.text_input("Teacher feedback", value=""),
    }

    if st.button("Add observation"):
        validate_child_profile(child_name, sex, int(age_years))
        manual_frame = growth_frame_from_manual_entry(manual_entry)
        validate_growth_frame(manual_frame)
        st.session_state.setdefault("growth_frame", pd.DataFrame())
        st.session_state["growth_frame"] = pd.concat([st.session_state["growth_frame"], manual_frame], ignore_index=True)
        st.success("Observation added.")
        st.dataframe(st.session_state["growth_frame"])
