# Day 21 테스트: adapter field 변환과 기존 detection pipeline 연결 검증

from week04.d21 import build_raw_detection, convert_detections


def test_build_raw_detection_converts_required_fields():
    model_detection = {
        "xyxy": [120, 80, 300, 220],
        "class_id": 0,
        "class_name": "vehicle",
        "confidence": 0.87,
    }

    expected_raw_detection = {
        "bbox": [120, 80, 300, 220],
        "class_id": 0,
        "className": "vehicle",
        "confidence": 0.87,
    }
    actual = build_raw_detection(model_detection)

    assert actual == expected_raw_detection


def test_adapter_output_connects_to_existing_detection_pipeline():
    model_detections = [
        {
            "xyxy": [120, 80, 300, 220],
            "class_id": 0,
            "class_name": "vehicle",
            "confidence": 0.87,
        },
        {
            "xyxy": [400, 100, 480, 280],
            "class_id": 1,
            "class_name": "person",
            "confidence": 0.76,
        },
    ]

    raw_results = [
        build_raw_detection(model_detection)
        for model_detection in model_detections
    ]

    detections = convert_detections(raw_results, 0.8)

    assert len(detections) == 1
    assert detections[0].className == "vehicle"
    assert detections[0].confidence == 0.87
