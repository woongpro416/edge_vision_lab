import pytest

from week02.d10 import filter_detections_by_confidence


def test_filter_keeps_detections_at_or_above_threshold():
    # TODO 1: vehicle 0.87, person 0.42, baggage 0.68을 담은 raw_results를 만든다.
    raw_results = [
    {"className": "vehicle", "confidence": 0.87},
    {"className": "person", "confidence": 0.42},
    {"className": "baggage", "confidence": 0.68},
]
    # TODO 2: threshold를 0.5로 만든다.
    threshold = 0.5
    # TODO 3: filter_detections_by_confidence() 실행 결과를 filtered_results에 담는다.
    filtered_results = filter_detections_by_confidence(raw_results, threshold)
    # TODO 4: vehicle과 baggage만 남은 expected_results를 만든다.
    expected_results = [
        {"className": "vehicle", "confidence": 0.87},
        {"className": "baggage", "confidence": 0.68},
    ]
    # TODO 5: filtered_results와 expected_results가 같은지 assert로 확인한다.
    # 이유: 기준 미만 detection이 filtering 후에도 남는 버그를 막는다.
    assert filtered_results == expected_results


def test_filter_includes_detection_equal_to_threshold():
    # TODO 1: vehicle 0.80, person 0.79를 담은 raw_results를 만든다.
    raw_results = [
    {"className": "vehicle", "confidence": 0.8},
    {"className": "person", "confidence": 0.79},
]
    # TODO 2: threshold를 0.8로 만든다.
    threshold = 0.8
    # TODO 3: filtering 결과를 만든다.
    filtered_results = filter_detections_by_confidence(raw_results, threshold)
    # TODO 4: vehicle 0.80만 남는지 assert로 확인한다.
    expected_results = [
    {"className": "vehicle", "confidence": 0.8},
]
    assert len(filtered_results) == 1
    # 이유: confidence >= threshold 계약에서 같은 값도 포함되는지 검증한다.
    assert filtered_results == expected_results

def test_filter_rejects_threshold_above_one():
    # TODO 1: 간단한 raw_results list를 만든다.
    raw_results = []
    # TODO 2: pytest.raises(ValueError) 블록을 만든다.
    with pytest.raises(ValueError):
        filter_detections_by_confidence(raw_results, threshold=1.1)
    # TODO 3: threshold=1.1로 filter_detections_by_confidence()를 호출한다.
    # 이유: 0.0~1.0 범위 밖 threshold가 조용히 통과하는 버그를 막는다.
