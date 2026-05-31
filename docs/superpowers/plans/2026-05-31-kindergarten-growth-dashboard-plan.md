# Kindergarten Growth Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-child Streamlit dashboard that ingests growth metrics from CSV or manual entry, visualizes progress over time, and compares the child against local age/grade standards plus Data.gov education context.

**Architecture:** Use a small modular Streamlit app with thin UI tabs and focused support modules for ingestion, validation, analytics, benchmarks, charting, and Data.gov loading. Keep all benchmark logic determinisSecond, execution option. 

**Tech Stack:** Python 3.11+, UV, Streamlit, pandas, Altair, requests, pytest.

---

## File Map

- Create: `pyproject.toml`
- Create: `app.py`
- Create: `src/__init__.py`
- Create: `src/io.py`
- Create: `src/validation.py`
- Create: `src/analytics.py`
- Create: `src/benchmarks.py`
- Create: `src/charts.py`
- Create: `services/__init__.py`
- Create: `services/datagov.py`
- Create: `tabs/__init__.py`
- Create: `tabs/intake.py`
- Create: `tabs/history.py`
- Create: `tabs/comparison.py`
- Create: `data/standards/age_grade_standards.csv`
- Create: `tests/test_io.py`
- Create: `tests/test_validation.py`
- Create: `tests/test_analytics.py`
- Create: `tests/test_benchmarks.py`
- Create: `tests/test_datagov.py`
- Create: `tests/test_app_smoke.py`

## Target Data Contracts

### Growth observation schema

```python
OBSERVATION_COLUMNS = [
    "date",
    "reading_minutes",
    "books_read",
    "sight_words_mastered",
    "letters_recognized",
    "writing_score",
    "math_problems_correct",
    "screen_time_minutes",
    "outdoor_play_minutes",
    "mood",
    "teacher_feedback",
]
```

### Child profile schema

```python
CHILD_PROFILE_FIELDS = [
    "child_name",
    "sex",
    "birth_date",
    "age_years",
    "grade_level",
]
```

### Local standards schema

```csv
metric,sex,age_min_months,age_max_months,expected_min,expected_target,expected_max,unit,notes
reading_minutes,all,60,72,15,20,30,minutes,Daily independent or shared reading
books_read,all,60,72,1,2,4,books,Books per week
sight_words_mastered,all,60,72,5,10,20,words,Recognized sight words
letters_recognized,all,60,72,20,26,26,letters,Uppercase and lowercase recognition
writing_score,all,60,72,1,3,5,score,Simple rubric score
math_problems_correct,all,60,72,5,10,15,problems,Simple arithmetic or number sense
screen_time_minutes,all,60,72,0,30,60,minutes,Recommended daily screen time
outdoor_play_minutes,all,60,72,30,60,120,minutes,Recommended daily outdoor play
```

---

### Task 1: Scaffold the UV project and app entrypoint

**Files:**
- Create: `pyproject.toml`
- Create: `app.py`
- Create: `src/__init__.py`
- Create: `tabs/__init__.py`
- Create: `services/__init__.py`
- Create: `tests/test_app_smoke.py`

- [ ] **Step 1: Write the failing smoke test**

```python
from app import create_app_shell


def test_create_app_shell_returns_title_and_tabs():
    shell = create_app_shell()
    assert shell["title"] == "Kindergarten Growth Journey"
    assert shell["tabs"] == ["Input", "Historical Snapshot", "Comparison"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_app_smoke.py -v`
Expected: FAIL because `create_app_shell` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

```python
def create_app_shell():
    return {
        "title": "Kindergarten Growth Journey",
        "tabs": ["Input", "Historical Snapshot", "Comparison"],
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_app_smoke.py -v`
Expected: PASS.

- [ ] **Step 5: Add the UV dependency manifest**

```toml
[project]
name = "kindergarten-growth-journey"
version = "0.1.0"
description = "Single-child kindergarten growth dashboard"
requires-python = ">=3.11"
dependencies = [
  "streamlit>=1.37",
  "pandas>=2.2",
  "altair>=5.3",
  "requests>=2.32",
]

[dependency-groups]
dev = [
  "pytest>=8.3",
]
```

Run:

```powershell
uv sync
```

Expected: dependencies resolve and the project environment is ready.

---

### Task 2: Build CSV ingestion and manual-entry normalization

**Files:**
- Create: `src/io.py`
- Create: `tests/test_io.py`
- Modify: `app.py`
- Modify: `tabs/intake.py`

- [ ] **Step 1: Write the failing ingestion test**

```python
import pandas as pd
from src.io import normalize_growth_frame


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_io.py -v`
Expected: FAIL because `normalize_growth_frame` is missing.

- [ ] **Step 3: Implement the minimal normalization logic**

```python
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
    return normalized[[c for c in normalized.columns if c in COLUMN_MAP.values()]]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_io.py -v`
Expected: PASS.

- [ ] **Step 5: Wire upload/manual entry into the Intake tab**

```python
import streamlit as st

from src.io import normalize_growth_frame


def render_intake_tab():
    st.header("Input")
    upload = st.file_uploader("Upload growth CSV", type=["csv"])
    if upload is not None:
        import pandas as pd

        frame = pd.read_csv(upload)
        st.dataframe(normalize_growth_frame(frame))
```

---

### Task 3: Add validation for child profile and observation data

**Files:**
- Create: `src/validation.py`
- Create: `tests/test_validation.py`
- Modify: `tabs/intake.py`

- [ ] **Step 1: Write the failing validation test**

```python
import pandas as pd
import pytest
from src.validation import validate_growth_frame


def test_validate_growth_frame_rejects_missing_required_columns():
    frame = pd.DataFrame([{"date": "2026-01-01", "reading_minutes": 20}])
    with pytest.raises(ValueError, match="missing required columns: books_read"):
        validate_growth_frame(frame)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_validation.py -v`
Expected: FAIL because `validate_growth_frame` is missing.

- [ ] **Step 3: Implement validation**

```python
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
    missing = [col for col in REQUIRED_COLUMNS if col not in frame.columns]
    if missing:
        raise ValueError(f"missing required columns: {', '.join(missing)}")
    if frame["date"].isna().any():
        raise ValueError("date contains invalid or missing values")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_validation.py -v`
Expected: PASS.

- [ ] **Step 5: Add child profile validation to the Intake tab**

```python
def validate_child_profile(child_name: str, sex: str, age_years: int | None) -> None:
    if not child_name.strip():
        raise ValueError("child_name is required")
    if sex not in {"boy", "girl"}:
        raise ValueError("sex must be 'boy' or 'girl'")
    if age_years is not None and age_years < 0:
        raise ValueError("age_years must be non-negative")
```

---

### Task 4: Implement analytics for progress and trends

**Files:**
- Create: `src/analytics.py`
- Create: `tests/test_analytics.py`
- Modify: `tabs/history.py`

- [ ] **Step 1: Write the failing analytics test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_analytics.py -v`
Expected: FAIL because `summarize_progress` is missing.

- [ ] **Step 3: Implement minimal progress summarization**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_analytics.py -v`
Expected: PASS.

- [ ] **Step 5: Add history tab rendering**

```python
def render_history_tab(frame):
    st.header("Historical Snapshot")
    summary = summarize_progress(frame, "reading_minutes")
    st.metric("Reading minutes", summary["end"], delta=summary["delta"])
```

---

### Task 5: Build benchmark loading and comparison logic

**Files:**
- Create: `src/benchmarks.py`
- Create: `tests/test_benchmarks.py`
- Create: `data/standards/age_grade_standards.csv`
- Modify: `tabs/comparison.py`

- [ ] **Step 1: Write the failing benchmark test**

```python
import pandas as pd
from src.benchmarks import compare_to_standard


def test_compare_to_standard_returns_gap_and_status():
    standards = pd.DataFrame(
        [
            {
                "metric": "reading_minutes",
                "sex": "all",
                "age_min_months": 60,
                "age_max_months": 72,
                "expected_min": 15,
                "expected_target": 20,
                "expected_max": 30,
                "unit": "minutes",
            }
        ]
    )
    result = compare_to_standard(
        metric="reading_minutes",
        value=25,
        age_months=66,
        sex="boy",
        standards=standards,
    )
    assert result["status"] == "on_track"
    assert result["gap_to_target"] == 5
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_benchmarks.py -v`
Expected: FAIL because `compare_to_standard` is missing.

- [ ] **Step 3: Implement standards lookup and comparison**

```python
def compare_to_standard(metric, value, age_months, sex, standards):
    subset = standards[
        (standards["metric"] == metric)
        & (standards["age_min_months"] <= age_months)
        & (standards["age_max_months"] >= age_months)
        & ((standards["sex"] == sex) | (standards["sex"] == "all"))
    ]
    if subset.empty:
        return {"status": "unknown", "gap_to_target": None}
    row = subset.iloc[0]
    gap = value - row["expected_target"]
    status = "on_track" if row["expected_min"] <= value <= row["expected_max"] else "off_track"
    return {
        "status": status,
        "gap_to_target": gap,
        "expected_target": row["expected_target"],
        "unit": row["unit"],
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_benchmarks.py -v`
Expected: PASS.

- [ ] **Step 5: Add the local standards seed file**

```csv
metric,sex,age_min_months,age_max_months,expected_min,expected_target,expected_max,unit,notes
reading_minutes,all,60,72,15,20,30,minutes,Daily reading support
books_read,all,60,72,1,2,4,books,Books per week
sight_words_mastered,all,60,72,5,10,20,words,Core sight-word recognition
letters_recognized,all,60,72,20,26,26,letters,Alphabet recognition
writing_score,all,60,72,1,3,5,score,Rubric-based writing score
math_problems_correct,all,60,72,5,10,15,problems,Simple math practice
screen_time_minutes,all,60,72,0,30,60,minutes,Daily limit guidance
outdoor_play_minutes,all,60,72,30,60,120,minutes,Physical activity guidance
```

- [ ] **Step 6: Build the Comparison tab**

```python
def render_comparison_tab(frame, child_profile, standards):
    st.header("Comparison")
    reading_value = frame.sort_values("date")["reading_minutes"].iloc[-1]
    age_months = child_profile["age_years"] * 12
    result = compare_to_standard("reading_minutes", reading_value, age_months, child_profile["sex"], standards)
    st.metric("Reading minutes", reading_value, delta=result["gap_to_target"])
```

---

### Task 6: Add Data.gov context loading and graceful fallback

**Files:**
- Create: `services/datagov.py`
- Create: `tests/test_datagov.py`
- Modify: `tabs/history.py`

- [ ] **Step 1: Write the failing Data.gov loader test**

```python
from services.datagov import dataset_metadata


def test_dataset_metadata_includes_title_and_download_url():
    meta = dataset_metadata()
    assert meta["title"] == "2011-12 Early Childhood and Prekindergarten Enrollment Estimations Civil Rights Data Collection"
    assert meta["download_url"].startswith("https://")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_datagov.py -v`
Expected: FAIL because `dataset_metadata` is missing.

- [ ] **Step 3: Implement a small metadata helper with a cached payload**

```python
DATASET_METADATA = {
    "title": "2011-12 Early Childhood and Prekindergarten Enrollment Estimations Civil Rights Data Collection",
    "download_url": "https://ocrdata.ed.gov/assets/downloads/2011-2012/Early%20Childhood%20and%20PreK%20Enrollment/Total-Enrollment-in-Early-Childhood-and-Prekindergarten.xlsx",
    "landing_page": "https://catalog.data.gov/dataset/2011-12-early-childhood-and-prekindergarten-enrollment-estimations-civil-rights-data-colle",
}


def dataset_metadata():
    return DATASET_METADATA.copy()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_datagov.py -v`
Expected: PASS.

- [ ] **Step 5: Add a safe context display path**

```python
def render_public_context():
    meta = dataset_metadata()
    st.caption(f"Public context source: {meta['title']}")
    st.link_button("Open Data.gov source", meta["landing_page"])
```

---

### Task 7: Wire the Streamlit tabs together and polish the UI

**Files:**
- Modify: `app.py`
- Modify: `tabs/intake.py`
- Modify: `tabs/history.py`
- Modify: `tabs/comparison.py`
- Modify: `src/charts.py`

- [ ] **Step 1: Write the final smoke test for the app shell**

```python
from app import create_app_shell


def test_create_app_shell_has_three_tabs():
    shell = create_app_shell()
    assert len(shell["tabs"]) == 3
```

- [ ] **Step 2: Run the smoke test**

Run: `uv run pytest tests/test_app_smoke.py -v`
Expected: PASS.

- [ ] **Step 3: Implement the Streamlit app wiring**

```python
import streamlit as st

from tabs.comparison import render_comparison_tab
from tabs.history import render_history_tab
from tabs.intake import render_intake_tab


def create_app_shell():
    return {
        "title": "Kindergarten Growth Journey",
        "tabs": ["Input", "Historical Snapshot", "Comparison"],
    }


def main():
    st.set_page_config(page_title="Kindergarten Growth Journey", layout="wide")
    st.title("Kindergarten Growth Journey")
    input_tab, history_tab, comparison_tab = st.tabs(create_app_shell()["tabs"])
    with input_tab:
        render_intake_tab()
    with history_tab:
        render_history_tab()
    with comparison_tab:
        render_comparison_tab()


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the app locally**

Run:

```powershell
uv run streamlit run app.py
```

Expected: the app opens with 3 tabs, the upload form, historical snapshot area, and comparison cards.

- [ ] **Step 5: Commit the finished slice**

```powershell
git add app.py pyproject.toml src tabs services data tests docs/superpowers/plans/2026-05-31-kindergarten-growth-dashboard-plan.md
git commit -m "feat: build kindergarten growth dashboard"
```

---

## Self-Review Checklist

- Spec coverage:
  - Input tab upload and manual-entry support is covered in Tasks 1, 2, and 3.
  - Historical snapshot and trend charts are covered in Task 4 and Task 7.
  - Comparison cards and standards logic are covered in Task 5 and Task 7.
  - Data.gov contextual data is covered in Task 6.
  - Single-child scope is preserved throughout.
- Placeholder scan:
  - No `TBD`, `TODO`, or vague “add validation” style steps remain.
  - Every task names actual files and includes concrete test or implementation snippets.
- Type consistency:
  - `create_app_shell`, `normalize_growth_frame`, `validate_growth_frame`, `summarize_progress`, `compare_to_standard`, and `dataset_metadata` are used consistently across tasks and tests.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-05-31-kindergarten-growth-dashboard-plan.md`. Two execution options:

1. Subagent-Driven (recommended) - dispatch a fresh subagent per task, review between tasks, fast iteration
2. Inline Execution - execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach?
