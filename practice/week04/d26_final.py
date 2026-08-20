# Day 26 독립 재구현: confidence filtering Happy/Empty 확인
import pytest

def filtering_result(detections: list[dict], threshold: float):
    results = []
    for detection in detections:
        if detection["confidence"] >= threshold:
            results.append(detection)

    return results


def test_happy_result():
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

    results = filtering_result(detections, threshold)
    print(results)
    assert len(results) == 1
    assert results[0]["confidence"] == 0.87
    return results

def test_empty_results():
    detection = []
    threshold = 0.8

    results = filtering_result(detection, threshold)
    print(results)
    assert results == []
    return results

test_empty_results()
test_happy_result()
