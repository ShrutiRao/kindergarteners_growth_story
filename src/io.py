from __future__ import annotations

import pandas as pd


COLUMN_MAP = {
    "Date": "date",
    "Reading_Minutes": "reading_minutes",
    "Books_Read": "books_read",
    "Sight_Words_Mastered": "sight_words_mastered",
    "Letters_Recognized": "letters_recognized",
    "Writing_Score": "writing_score",
    "Math_Problems_Correct": "math_problems_correct",
    "Screen_Time_Minutes": "screen_time_minutes",
    "Outdoor_Play_Minutes": "outdoor_play_minutes",
    "Mood": "mood",
    "Teacher_Feedback": "teacher_feedback",
}


def normalize_growth_frame(frame: pd.DataFrame) -> pd.DataFrame:
    normalized = frame.rename(columns=COLUMN_MAP).copy()
    if "date" in normalized.columns:
        normalized["date"] = pd.to_datetime(normalized["date"], errors="coerce")
    ordered_columns = [column for column in COLUMN_MAP.values() if column in normalized.columns]
    return normalized[ordered_columns]


def growth_frame_from_manual_entry(entry: dict) -> pd.DataFrame:
    frame = pd.DataFrame([entry])
    return normalize_growth_frame(frame)


def growth_template_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Date": None,
                "Reading_Minutes": None,
                "Books_Read": None,
                "Sight_Words_Mastered": None,
                "Letters_Recognized": None,
                "Writing_Score": None,
                "Math_Problems_Correct": None,
                "Screen_Time_Minutes": None,
                "Outdoor_Play_Minutes": None,
                "Mood": None,
                "Teacher_Feedback": None,
            }
        ]
    )
