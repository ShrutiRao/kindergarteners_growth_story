import pandas as pd

from src.analytics import summarize_progress


def test_summarize_progress_reports_start_end_and_delta():
    frame = pd.DataFrame(
        [
            {"date": "2026-01-01", "reading_minutes": 20},
            {"date": "2026-01-08", "reading_minutes": 30},
        ]
    )
    summary = summarize_progress(frame, metric="reading_minutes")
    assert summary["start"] == 20
    assert summary["end"] == 30
    assert summary["delta"] == 10
