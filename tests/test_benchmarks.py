import pandas as pd

from src.benchmarks import benchmark_overview, compare_to_standard


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


def test_benchmark_overview_returns_primary_metric_cards():
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
            },
            {
                "metric": "books_read",
                "sex": "all",
                "age_min_months": 60,
                "age_max_months": 72,
                "expected_min": 1,
                "expected_target": 2,
                "expected_max": 4,
                "unit": "books",
            },
        ]
    )
    frame = pd.DataFrame(
        [
            {
                "date": "2026-01-01",
                "reading_minutes": 20,
                "books_read": 1,
            },
            {
                "date": "2026-01-08",
                "reading_minutes": 25,
                "books_read": 3,
            },
        ]
    )
    overview = benchmark_overview(
        frame=frame,
        child_profile={"sex": "boy", "age_years": 5},
        standards=standards,
        metrics=["reading_minutes", "books_read"],
    )
    assert [item["metric"] for item in overview] == ["reading_minutes", "books_read"]
    assert overview[0]["status"] == "on_track"
    assert overview[1]["gap_to_target"] == 1
