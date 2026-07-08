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

    #TODO 1:  rows 를 DataFrame으로 변환
    df = pd.DataFrame(rows)
    #TODO 2: 컬럼 순서를 COLUMNS 기준으로 맞추기
    df = df[COLUMNS]
    #TODO 3: df 반환
    return df

def count_by_zones(df: pd.DataFrame) -> pd.DataFrame:
    #TODO : zone 별 이벤트 개수 세기
    events = df.groupby("zone").size().reset_index(name="counts")
    return events

def sort_by_confidence_desc(df: pd.DataFrame) -> pd.DataFrame:
    #TODO : confidence 기준 내림차순 정렬
    sorted_desc = df.sort_values("confidence", ascending=False)
    return sorted_desc

def filter_high_confidence(df: pd.DataFrame, min_confidence: float) -> pd.DataFrame:
    #TODO 1: confidence가 min_confidence 이상인지 mask 만들기
    mask = df["confidence"] >= min_confidence
    #TODO 2: df[mask]반환
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


    #TODO assert 3개 작성
    #1. 전체 row 개수는 5개인가?
    assert len(df) == 5
    #2. gate_b 이벤트는 2개인가?
    gate_b_count = (df["zone"] == "gate_b").sum()
    assert gate_b_count == 2
    #3. high_confidence_events에는 confidence 0.8 미만이 없는가?
    assert (high_confidence_events["confidence"] >= 0.8).all()