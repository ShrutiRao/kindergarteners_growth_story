import pandas as pd

from src.io import growth_template_frame, normalize_growth_frame


def test_normalize_growth_frame_lowers_columns_and_parses_date():
    raw = pd.DataFrame(
        [
            {
                "Date": "2026-01-01",
                "Reading_Minutes": 20,
                "Books_Read": 1,
                "Mood": "Happy",
            }
        ]
    )
    normalized = normalize_growth_frame(raw)
    assert list(normalized.columns) == ["date", "reading_minutes", "books_read", "mood"]
    assert str(normalized.loc[0, "date"].date()) == "2026-01-01"


def test_growth_template_frame_exposes_expected_columns():
    template = growth_template_frame()
    assert list(template.columns) == [
        "Date",
        "Reading_Minutes",
        "Books_Read",
        "Sight_Words_Mastered",
        "Letters_Recognized",
        "Writing_Score",
        "Math_Problems_Correct",
        "Screen_Time_Minutes",
        "Outdoor_Play_Minutes",
        "Mood",
        "Teacher_Feedback",
    ]
    assert len(template) == 1
