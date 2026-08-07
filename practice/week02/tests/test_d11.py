# ?? ??: Day 11 Tests ? filtered inference response contract? pytest? ?????.

import pytest

from week02.d11 import build_filtered_inference_response


def test_build_filtered_response_happy_path():
    raw_results = [
        {"className": "vehicle", "confidence": 0.87},
        {"className": "person", "confidence": 0.76},
    ]

    filtered_results = [{"className": "vehicle", "confidence": 0.87}]

    threshold = 0.8

    response = build_filtered_inference_response(
        raw_results, filtered_results, threshold)

    assert response["rawDetectionCount"] == 2
    assert response["detectionCount"] == 1
    assert response["confidenceThreshold"] == 0.8
    assert response["classCounts"] == {"vehicle": 1}


def test_empty_filtered_results():
    raw_results = [
        {"className": "vehicle", "confidence": 0.87},
        {"className": "person", "confidence": 0.76},
    ]

    filtered_results = []

    threshold = 0.8

    response = build_filtered_inference_response(
        raw_results, filtered_results, threshold)

    assert response["status"] == "OK"
    assert response["rawDetectionCount"] == 2
    assert response["detectionCount"] == 0
    assert response["classCounts"] == {}
    assert response["results"] == []


def test_filtered_results_cannot_be_longer_than_raw_results():
    raw_results = [
        {"className": "vehicle", "confidence": 0.87}
    ]

    filtered_results = [
        {"className": "vehicle", "confidence": 0.87},
        {"className": "person", "confidence": 0.76},
    ]

    threshold = 0.8

    with pytest.raises(ValueError):
        build_filtered_inference_response(raw_results, filtered_results, threshold)
