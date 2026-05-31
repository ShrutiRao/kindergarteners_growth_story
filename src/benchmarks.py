from __future__ import annotations

from pathlib import Path

import pandas as pd


STANDARDS_PATH = Path("data/standards/age_grade_standards.csv")
PRIMARY_METRICS = [
    "reading_minutes",
    "books_read",
    "sight_words_mastered",
    "letters_recognized",
    "writing_score",
    "math_problems_correct",
]


def load_age_grade_standards(path: Path | str = STANDARDS_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


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
        "expected_min": row["expected_min"],
        "expected_max": row["expected_max"],
    }


def benchmark_overview(frame: pd.DataFrame, child_profile: dict, standards: pd.DataFrame, metrics: list[str] | None = None) -> list[dict]:
    metrics = metrics or PRIMARY_METRICS
    ordered = frame.sort_values("date")
    latest = ordered.iloc[-1]
    age_months = int(child_profile["age_years"]) * 12
    overview = []
    for metric in metrics:
        if metric not in latest.index:
            continue
        result = compare_to_standard(
            metric=metric,
            value=float(latest[metric]),
            age_months=age_months,
            sex=child_profile["sex"],
            standards=standards,
        )
        overview.append(
            {
                "metric": metric,
                "value": float(latest[metric]),
                "status": result["status"],
                "gap_to_target": result.get("gap_to_target"),
                "expected_target": result.get("expected_target"),
                "unit": result.get("unit"),
            }
        )
    return overview
