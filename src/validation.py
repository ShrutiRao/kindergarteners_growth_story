from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "reading_minutes",
    "books_read",
    "sight_words_mastered",
    "letters_recognized",
    "writing_score",
    "math_problems_correct",
    "screen_time_minutes",
    "outdoor_play_minutes",
]


def validate_growth_frame(frame: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")

    if frame["date"].isna().any():
        raise ValueError("date contains invalid or missing values")

    numeric_columns = [column for column in REQUIRED_COLUMNS if column != "date"]
    for column in numeric_columns:
        if not pd.api.types.is_numeric_dtype(frame[column]):
            raise ValueError(f"{column} must be numeric")


def validate_child_profile(child_name: str, sex: str, age_years: int | None) -> None:
    if not child_name.strip():
        raise ValueError("child_name is required")
    if sex not in {"boy", "girl"}:
        raise ValueError("sex must be 'boy' or 'girl'")
    if age_years is not None and age_years < 0:
        raise ValueError("age_years must be non-negative")
