import pandas as pd

from src.analytics import activity_minutes_by_day


def test_activity_minutes_by_day_reshapes_minutes_columns():
    frame = pd.DataFrame(
        [
            {
                "date": "2026-01-01",
                "reading_minutes": 20,
                "screen_time_minutes": 45,
                "outdoor_play_minutes": 60,
            }
        ]
    )

    activity_frame = activity_minutes_by_day(frame)

    assert list(activity_frame["activity"]) == ["Reading", "Screen Time", "Outdoor Play"]
    assert list(activity_frame["minutes"]) == [20, 45, 60]
