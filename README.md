# Kindergarten Growth Journey

A single-child Streamlit dashboard for tracking kindergarten growth metrics over time, comparing progress against local age/grade standards, and viewing public education context.

## What it does

- Upload a CSV of growth observations
- Enter a new observation manually
- Store child profile details such as name, sex, age, and grade level
- Show a historical snapshot of progress over time
- Compare the child against age/grade standards
- Display contextual public education references from Data.gov
- Offer a downloadable CSV template for easier data entry

## Tech Stack

- Python
- Streamlit
- pandas
- Altair
- requests
- pytest
- UV for dependency management

## Project Layout

```text
kindergarteners_growth_story/
├─ app.py
├─ data/
│  └─ standards/
│     └─ age_grade_standards.csv
├─ docs/
│  └─ superpowers/
│     ├─ plans/
│     └─ specs/
├─ services/
│  └─ datagov.py
├─ src/
│  ├─ analytics.py
│  ├─ benchmarks.py
│  ├─ charts.py
│  ├─ io.py
│  └─ validation.py
├─ tabs/
│  ├─ comparison.py
│  ├─ history.py
│  └─ intake.py
└─ tests/
```

## Requirements

- Python 3.11 or newer
- UV installed locally

## Install

From the project root:

```powershell
uv sync
```

## Run the App

```powershell
uv run streamlit run app.py
```

## Run Tests

```powershell
uv run pytest -v
```

## Data Format

The app expects a CSV with columns similar to:

- `Date`
- `Reading_Minutes`
- `Books_Read`
- `Sight_Words_Mastered`
- `Letters_Recognized`
- `Writing_Score`
- `Math_Problems_Correct`
- `Screen_Time_Minutes`
- `Outdoor_Play_Minutes`
- `Mood`
- `Teacher_Feedback`

You can also use the built-in manual entry form on the Input tab.

## Notes

- The app is designed for a single child only.
- Local standards live in `data/standards/age_grade_standards.csv`.
- Data.gov context is loaded through a lightweight service layer so the app can still work if public data is unavailable.
