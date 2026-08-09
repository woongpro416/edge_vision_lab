# Day 16 테스트: confidence filtering과 DetectionResult DTO validation을 검증한다.

from week03.d16 import convert_detections, DetectionResult
import pytest
from pydantic import ValidationError


def test_convert_detections_threshold_0_8():
    raw_results = [
        {
            "bbox": [120, 80, 300, 220],
            "class_id": 0,
            "className": "vehicle",
            "confidence": 0.87,
        },
        {"bbox": [400, 100, 480, 280],
         "class_id": 1,
         "className": "person",
         "confidence": 0.76,
         }
    ]

    threshold = 0.8

    detections = convert_detections(raw_results, threshold)

    assert len(detections) == 1
    assert isinstance(detections[0], DetectionResult)
    assert detections[0].className == "vehicle"
    assert detections[0].confidence == 0.87


def test_convert_detections_threshold_0_7():
    raw_results = [
        {
            "bbox": [120, 80, 300, 220],
            "class_id": 0,
            "className": "vehicle",
            "confidence": 0.87,
        },
        {"bbox": [400, 100, 480, 280],
         "class_id": 1,
         "className": "person",
         "confidence": 0.76,
         }
    ]

    threshold = 0.7

    detections = convert_detections(raw_results, threshold)

    assert len(detections) == 2
    assert isinstance(detections[0], DetectionResult)
    assert isinstance(detections[1], DetectionResult)
    assert detections[0].className == "vehicle"
    assert detections[1].className == "person"
    assert detections[0].confidence == 0.87


def test_detection_result_rejects_invalid_confidence():
    invalid_detection = {
        "bbox": [120, 80, 300, 220],
        "class_id": 0,
        "className": "vehicle",
        "confidence": 1.2,
    }

    with pytest.raises(ValidationError):
        DetectionResult(**invalid_detection)
