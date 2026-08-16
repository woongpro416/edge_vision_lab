# Day 23 테스트: 가짜 YOLO Results로 Adapter 계약과 filtering 연결을 검증한다.
from types import SimpleNamespace

import torch

from week03.d16 import convert_detections
from week04.d23_real_yolo_adapter import build_raw_detections_from_yolo_result


def make_fake_yolo_result():
    xyxy_boxes = torch.tensor(
        [
            [10.8, 20.2, 110.6, 220.4],
            [300.0, 100.0, 400.0, 250.0],
        ],
        dtype=torch.float64
    )

    class_ids = torch.tensor(
        [0.0, 2.0],
        dtype=torch.float64,
    )

    confidences = torch.tensor(
        [0.91, 0.72],
        dtype=torch.float64,
    )

    boxes = SimpleNamespace(
        xyxy=xyxy_boxes,
        cls=class_ids,
        conf=confidences,
    )

    return SimpleNamespace(
        boxes=boxes,
        names={
            0: "person",
            2: "car",
        },
    )


def test_adapter_converts_mock_yolo_result_to_raw_results():
    fake_result = make_fake_yolo_result()

    actual_raw_results = build_raw_detections_from_yolo_result(fake_result)

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

    assert actual_raw_results == expected_raw_results


def test_adapter_output_connects_to_convert_detections():
    fake_result = make_fake_yolo_result()

    raw_results = build_raw_detections_from_yolo_result(fake_result)
    threshold = 0.8

    detections = convert_detections(raw_results, threshold)

    assert len(detections) == 1
    assert detections[0].className == "person"
    assert detections[0].confidence == 0.91
