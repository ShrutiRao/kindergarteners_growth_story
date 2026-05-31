from __future__ import annotations


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


def latest_observation(frame):
    if frame.empty:
        return None
    return frame.sort_values("date").iloc[-1]
