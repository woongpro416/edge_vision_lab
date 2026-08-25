# Day 28 테스트: Adapter Mapping, Pipeline, Empty, Boundary Contract를 검증한다.
from week03.d16 import DetectionResult
from week04.d28 import adapt_model_results, build_dto_detections


def test_adapt_mapping():
    detections = [{
        "xyxy": [120, 80, 360, 420],
        "class_id": 0,
        "class_name": "person",
        "confidence": 0.91,
    }]

    mapping_results = adapt_model_results(detections)

    assert len(mapping_results) == 1
    assert mapping_results[0]["bbox"] == [120, 80, 360, 420]
    assert mapping_results[0]["className"] == "person"


def test_pipeline_happy():
    model_results = [
        {
            "xyxy": [120, 80, 360, 420],
            "class_id": 0,
            "class_name": "person",
            "confidence": 0.91,
        },
        {
            "xyxy": [400, 150, 620, 510],
            "class_id": 1,
            "class_name": "vehicle",
            "confidence": 0.76,
        },
        {
            "xyxy": [700, 210, 810, 390],
            "class_id": 2,
            "class_name": "baggage",
            "confidence": 0.58,
        },
    ]

    threshold = 0.70

    happy_results = build_dto_detections(model_results, threshold)

    assert len(happy_results) == 2
    assert isinstance(happy_results[0], DetectionResult)
    assert happy_results[0].className == "person"
    assert happy_results[1].className == "vehicle"


def test_empty():
    detections = []
    threshold = 0.70

    empty_results = build_dto_detections(detections, threshold)

    assert empty_results == []


def test_boundary():
    detections = [{
        "xyxy": [120, 80, 360, 420],
        "class_id": 0,
        "class_name": "person",
        "confidence": 0.91,
    }]

    threshold = 0.91

    boundary_results = build_dto_detections(detections, threshold)

    assert len(boundary_results) == 1
