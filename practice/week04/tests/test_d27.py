# Day 27 학습: Filtering Service Contract와 Invalid Boundary pytest
from week04.d27 import build_filtered_results


def test_happy_case_detections():
    detections = [
        {
            "bbox": [100, 300, 200, 400],
            "class_id": 0,
            "className": 'person',
            "confidence": 0.87,
        },
        {
            "bbox": [200, 400, 300, 500],
            "class_id": 1,
            "className": 'car',
            "confidence": 0.72,
        },
        {
            "bbox": [30, 50, 80, 120],
            "class_id": 2,
            "className": 'airplane',
            "confidence": 0.62,
        },
    ]

    threshold = 0.8

    results = build_filtered_results(detections, threshold)

    assert len(results) == 1
    assert results[0]["confidence"] == 0.87


def test_empty_case_detections():
    detections = []
    threshold = 0.8

    empty_results = build_filtered_results(detections, threshold)

    assert empty_results == []


def test_boundary_case_detection():
    detections = [
        {
            "bbox": [100, 300, 200, 400],
            "class_id": 0,
            "className": 'person',
            "confidence": 0.80,
        },
    ]

    threshold = 0.80

    equal_result = build_filtered_results(detections, threshold)

    assert equal_result[0]["confidence"] == threshold
    assert len(equal_result) == 1
