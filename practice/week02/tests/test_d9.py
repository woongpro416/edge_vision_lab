# ?? ??: Day 09 Tests ? mock inference response? class counting? pytest? ?????.

import pytest

from week02.d9 import build_inference_response, count_detections_by_class


def test_build_inference_response_allows_empty_results():
    raw_results = []
    response = build_inference_response(raw_results)

    assert response["status"] == "OK"
    assert response["detectionCount"] == 0
    assert response["results"] == raw_results
    assert response["classCounts"] == {}


def test_build_inference_response_rejects_none():
    with pytest.raises(ValueError):
        build_inference_response(None)


def test_count_detections_by_class_counts_repeated_classes():
    raw_results = [
        {"className": "vehicle", "confidence": 0.87},
        {"className": "person", "confidence": 0.76},
        {"className": "vehicle", "confidence": 0.91},
    ]

    class_counts = count_detections_by_class(raw_results)
    expected_class_counts = {"vehicle": 2, "person": 1}

    assert class_counts == expected_class_counts


def test_count_detections_by_class_allows_empty_results():
    raw_results = []
    class_counts = count_detections_by_class(raw_results)

    assert class_counts == {}
