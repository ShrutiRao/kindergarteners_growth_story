# Kindergarten Growth Dashboard Design

## Summary
Build a Streamlit dashboard for a single kindergartner that accepts growth metrics from a CSV upload or manual entry, then visualizes progress over time and compares the child against two benchmark layers:

1. Public historical education context from Data.gov
2. Age/grade standards stored locally in a reference table

The app will be organized into 3 tabs:

- Input
- Historical Snapshot
- Comparison

## Goals

- Support one child only for the first version
- Accept the existing CSV format as the primary bulk import path
- Allow manual metric entry for quick updates
- Capture child profile data such as sex, age, and optionally grade level
- Show growth over time using trends and summaries
- Compare the child to age/grade expectations and public context
- Keep the app lightweight, easy to extend, and easy to understand

## Non-Goals

- Multi-child accounts or family dashboards
- Authentication or user management
- Writing data back to a remote database
- Fully automated ingestion of all Data.gov education datasets
- Medical or developmental diagnosis

## Assumptions

- The CSV in the repository is representative of the imported structure
- Age/grade standards can be stored in a local CSV and updated without code changes
- Data.gov data will be used as contextual reference data, not as a strict medical or educational standard
- The dashboard is intended for exploratory monitoring, not formal assessment

## User Flow

1. The user opens the dashboard.
2. In the Input tab, the user uploads a CSV or enters a new observation manually.
3. The app validates and normalizes the data.
4. The app stores the observations in session state for the current run.
5. The Historical Snapshot tab shows progress over time and summary movement.
6. The Comparison tab shows metric cards, standards gaps, and benchmark lines.

## Data Model

### Child profile

- `child_name`
- `sex`
- `birth_date` or `age_years`
- `grade_level` if available

### Growth observation

Based on the sample CSV, each record should support:

- `date`
- `reading_minutes`
- `books_read`
- `sight_words_mastered`
- `letters_recognized`
- `writing_score`
- `math_problems_correct`
- `screen_time_minutes`
- `outdoor_play_minutes`
- `mood`
- `teacher_feedback`

### Benchmark data

Two benchmark sources will be supported:

- `age_grade_standards.csv`: local reference table with expected ranges or targets
- Data.gov education datasets: public context data fetched or cached through a service layer

## Architecture

### Streamlit app structure

- `app.py`
  - creates the page shell and tab layout
  - wires together the child profile, upload, and chart components

- `tabs/intake.py`
  - CSV upload
  - manual entry form
  - child profile inputs
  - validation feedback

- `tabs/history.py`
  - time-series summaries
  - progress snapshots
  - historical trend charts

- `tabs/comparison.py`
  - benchmark comparison cards
  - standards gap display
  - progress-versus-standard charts

- `src/io.py`
  - read CSV input
  - normalize column names
  - unify upload and manual-entry records into one table

- `src/validation.py`
  - validate required fields
  - enforce numeric ranges
  - check date ordering
  - surface user-friendly errors

- `src/analytics.py`
  - compute summary statistics
  - trend direction
  - week-over-week or month-over-month deltas
  - baseline comparisons

- `src/benchmarks.py`
  - load local age/grade standards
  - compute benchmark deltas
  - prepare comparison metrics

- `src/charts.py`
  - create reusable chart functions
  - line charts for progress
  - bar or bullet-style benchmark views

- `services/datagov.py`
  - fetch or load cached public education reference data
  - isolate network and parsing logic away from the UI

## File Structure

```text
kindergarteners_growth_story/
├─ app.py
├─ pyproject.toml
├─ kindergarten_growth_metrics.csv
├─ data/
│  ├─ standards/
│  │  └─ age_grade_standards.csv
│  ├─ raw/
│  └─ processed/
├─ src/
│  ├─ __init__.py
│  ├─ io.py
│  ├─ validation.py
│  ├─ analytics.py
│  ├─ benchmarks.py
│  └─ charts.py
├─ tabs/
│  ├─ __init__.py
│  ├─ intake.py
│  ├─ history.py
│  └─ comparison.py
├─ services/
│  ├─ __init__.py
│  └─ datagov.py
└─ docs/
   └─ superpowers/
      └─ specs/
         └─ 2026-05-31-kindergarten-growth-dashboard-design.md
```

## Tab Design

### Tab 1: Input

This tab will let the user:

- upload a CSV
- enter one observation manually
- select sex
- provide age or birth date
- optionally provide grade level

The app should normalize uploaded and manual data to the same schema so downstream tabs do not care where the data came from.

### Tab 2: Historical Snapshot

This tab will show:

- a timeline of the child’s metrics
- summary cards for key changes
- recent trend direction for each core metric
- contextual public education indicators from Data.gov

The goal is to answer, “How has this child changed over time, and what context do we have around those changes?”

### Tab 3: Comparison

This tab will show:

- metric cards for selected indicators
- expected-versus-observed comparisons
- standard gap indicators
- trend lines against the local age/grade benchmark

The goal is to answer, “How is the child doing relative to expected norms and targets?”

## Benchmark Strategy

The comparison layer will use two reference types:

1. Local age/grade standards
   - Preferred for direct comparison
   - Stored in a local file so the app remains stable
   - Can define target ranges, minimums, or expected growth rates

2. Data.gov education data
   - Used as contextual background
   - Helpful for historical or national trend framing
   - Kept behind a service layer so the app can still run if the data cannot be refreshed

The app should clearly distinguish between “standards” and “context” so the user does not confuse the two.

## Error Handling

- If a CSV is missing required columns, show a readable validation message and list the missing fields
- If dates are out of order or malformed, reject the record and explain the issue
- If a metric is non-numeric where numeric data is required, show the offending field
- If Data.gov data cannot be loaded, degrade gracefully and continue using local standards only

## Testing Strategy

- CSV parsing tests for header normalization and sample input compatibility
- Validation tests for missing fields, invalid dates, and invalid numeric values
- Benchmark tests for age/grade comparison logic
- Analytics tests for trend and delta calculations
- Smoke test for the Streamlit app structure and tab rendering

## Acceptance Criteria

- The app has 3 working tabs
- The user can upload the provided CSV format successfully
- The user can add at least one observation manually
- The app accepts sex and age/birth-date inputs
- The Historical Snapshot tab shows time-based progress
- The Comparison tab shows metric cards and benchmark comparisons
- The app combines local age/grade standards with Data.gov context cleanly

## Open Questions

- Which specific Data.gov education dataset should be used first for the contextual layer?
- Should age be entered as exact birth date, current age in years, or both?
- Which metrics should be promoted to the “primary” comparison cards on the third tab?
