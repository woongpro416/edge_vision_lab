# Day 22 테스트: YOLO-style Adapter의 field 변환과 기존 filtering pipeline 연결

from week04.d22 import build_raw_detections_from_yolo_fields
from week03.d16 import convert_detections


def test_yolo_fields_are_converted_to_raw_results():
    xyxy_boxes = [
        [10.8, 20.2, 110.6, 220.4],
        [300.0, 100.0, 400.0, 250.0],
    ]
    class_ids = [0.0, 2.0]
    confidences = [0.91, 0.72]
    names = {
        0: "person",
        2: "car",
    }

    expected_raw_results = [
        {
            "bbox": [10, 20, 110, 220],
            "class_id": 0,
            "className": "person",
            "confidence": 0.91,
        },
        {
            "bbox": [300, 100, 400, 250],
            "class_id": 2,
            "className": "car",
            "confidence": 0.72,
        },
    ]

    actual_raw_results = build_raw_detections_from_yolo_fields(
        xyxy_boxes, class_ids, confidences, names
    )

    assert actual_raw_results == expected_raw_results


def test_adapter_output_connects_to_convert_detections():
    xyxy_boxes = [
        [10.8, 20.2, 110.6, 220.4],
        [300.1, 100.7, 400.9, 250.3],
    ]
    class_ids = [0.0, 2.0]
    confidences = [0.91, 0.72]
    names = {
        0: "person",
        2: "car",
    }
    threshold = 0.8

    raw_results = build_raw_detections_from_yolo_fields(
        xyxy_boxes, class_ids, confidences, names
    )

    detections = convert_detections(raw_results, threshold)

    assert len(detections) == 1
    assert detections[0].className == "person"
    assert detections[0].confidence == 0.91
