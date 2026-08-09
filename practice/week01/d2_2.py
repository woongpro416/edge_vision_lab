# 학습 요약: Day 02 — pandas DataFrame의 groupby와 confidence filtering을 연습한다.

import pandas as pd

COLUMNS = ["event_id", "zone", "event_type", "severity", "confidence"]

def build_event_dataframe() -> pd.DataFrame:
    rows = [
        {"event_id": "E001", "zone": "gate_a", "event_type": "vehicle", "severity": "low", "confidence": 0.72},
        {"event_id": "E002", "zone": "gate_b", "event_type": "person", "severity": "medium", "confidence": 0.91},
        {"event_id": "E003", "zone": "gate_a", "event_type": "vehicle", "severity": "high", "confidence": 0.86},
        {"event_id": "E004", "zone": "runway", "event_type": "object", "severity": "high", "confidence": 0.64},
        {"event_id": "E005", "zone": "gate_b", "event_type": "person", "severity": "low", "confidence": 0.83},
    ]


    df = pd.DataFrame(rows)

    df = df[COLUMNS]

    return df

def count_by_zones(df: pd.DataFrame) -> pd.DataFrame:

    events = df.groupby("zone").size().reset_index(name="counts")
    return events

def sort_by_confidence_desc(df: pd.DataFrame) -> pd.DataFrame:

    sorted_desc = df.sort_values("confidence", ascending=False)
    return sorted_desc

def filter_high_confidence(df: pd.DataFrame, min_confidence: float) -> pd.DataFrame:

    mask = df["confidence"] >= min_confidence

    df = df[mask]
    return df


if __name__ == "__main__":
    df = build_event_dataframe()

    zone_counts = count_by_zones(df)
    sorted_by = sort_by_confidence_desc(df)
    high_confidence_events = filter_high_confidence(df, min_confidence=0.8)

    print(df)
    print(zone_counts)
    print(sorted_by)
    print(high_confidence_events)




    assert len(df) == 5

    gate_b_count = (df["zone"] == "gate_b").sum()
    assert gate_b_count == 2

    assert (high_confidence_events["confidence"] >= 0.8).all()
