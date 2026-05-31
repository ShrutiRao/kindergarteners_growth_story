import pandas as pd
import pytest

from src.validation import validate_growth_frame


def test_validate_growth_frame_rejects_missing_required_columns():
    frame = pd.DataFrame([{"date": "2026-01-01", "reading_minutes": 20}])
    with pytest.raises(ValueError, match="missing required columns: books_read"):
        validate_growth_frame(frame)
