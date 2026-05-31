from __future__ import annotations

import pandas as pd


def summarize_progress(frame, metric: str) -> dict:
    ordered = frame.sort_values("date")
    values = ordered[metric].dropna().tolist()
    if not values:
        return {"start": None, "end": None, "delta": None}
    return {
        "start": values[0],
        "end": values[-1],
        "delta": values[-1] - values[0],
    }


def latest_observation(frame):
    if frame.empty:
        return None
    return frame.sort_values("date").iloc[-1]


def teacher_feedback_sentiment(feedback: str) -> str:
    text = (feedback or "").strip().lower()
    if not text:
        return "neutral"

    positive_keywords = [
        "excellent",
        "great",
        "improved",
        "confident",
        "confidence",
        "proud",
        "strong effort",
        "well",
        "good",
        "progress",
        "participated",
        "engaged",
        "focused",
        "thoughtful",
        "curious",
        "worked well",
    ]
    support_keywords = [
        "struggle",
        "needs help",
        "needs support",
        "concern",
        "difficulty",
        "challenging",
        "interrupted",
        "off task",
        "incomplete",
        "late",
        "not yet",
        "requires support",
    ]

    if any(keyword in text for keyword in support_keywords):
        return "needs_support"
    if any(keyword in text for keyword in positive_keywords):
        return "positive"
    return "neutral"


def mood_feedback_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    working = frame.copy()
    working["feedback_sentiment"] = working["teacher_feedback"].fillna("").map(teacher_feedback_sentiment)
    matrix = pd.crosstab(working["mood"], working["feedback_sentiment"]).sort_index()
    return matrix


def activity_minutes_by_day(frame: pd.DataFrame) -> pd.DataFrame:
    activity_map = {
        "reading_minutes": "Reading",
        "screen_time_minutes": "Screen Time",
        "outdoor_play_minutes": "Outdoor Play",
    }
    available = [column for column in activity_map if column in frame.columns]
    if not available:
        return pd.DataFrame(columns=["date", "activity", "minutes"])

    working = frame.loc[:, ["date", *available]].copy()
    long_frame = working.melt(id_vars="date", var_name="activity", value_name="minutes")
    long_frame["activity"] = long_frame["activity"].map(activity_map)
    return long_frame.dropna(subset=["minutes"])
