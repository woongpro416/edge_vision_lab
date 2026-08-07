# ?? ??: Day 10 Tests ? confidence threshold filtering? ???? pytest? ?????.

import pytest

from week02.d10 import filter_detections_by_confidence


def test_filter_keeps_detections_at_or_above_threshold():

    raw_results = [
    {"className": "vehicle", "confidence": 0.87},
    {"className": "person", "confidence": 0.42},
    {"className": "baggage", "confidence": 0.68},
]

    threshold = 0.5

    filtered_results = filter_detections_by_confidence(raw_results, threshold)

    expected_results = [
        {"className": "vehicle", "confidence": 0.87},
        {"className": "baggage", "confidence": 0.68},
    ]


    assert filtered_results == expected_results


def test_filter_includes_detection_equal_to_threshold():

    raw_results = [
    {"className": "vehicle", "confidence": 0.8},
    {"className": "person", "confidence": 0.79},
]

    threshold = 0.8

    filtered_results = filter_detections_by_confidence(raw_results, threshold)

    expected_results = [
    {"className": "vehicle", "confidence": 0.8},
]
    assert len(filtered_results) == 1

    assert filtered_results == expected_results

def test_filter_rejects_threshold_above_one():

    raw_results = []

    with pytest.raises(ValueError):
        filter_detections_by_confidence(raw_results, threshold=1.1)
