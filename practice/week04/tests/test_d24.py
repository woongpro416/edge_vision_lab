# Day 24 테스트: 가짜 YOLO Result가 Adapter 계약에 맞게 변환되는지 확인한다.
from types import SimpleNamespace

import torch

from week04.d24_review import build_raw_detections_from_yolo_result


def make_fake_yolo_result() -> SimpleNamespace:
    """2개의 detection을 가진, 실제 YOLO Result 모양의 가짜 객체를 만든다."""
    boxes = SimpleNamespace(
        xyxy=torch.tensor(
            [[10.8, 20.2, 110.6, 220.4], [300.0, 100.0, 400.0, 250.0]],
            dtype=torch.float64,
        ),
        cls=torch.tensor([0.0, 2.0], dtype=torch.float64),
        conf=torch.tensor([0.91, 0.72], dtype=torch.float64),
    )
    return SimpleNamespace(
        boxes=boxes,
        names={0: "person", 2: "car"},
    )


def make_empty_yolo_result() -> SimpleNamespace:
    """detection이 0건인 가짜 YOLO Result를 만든다."""
    boxes = SimpleNamespace(
        xyxy=torch.empty((0, 4), dtype=torch.float64),
        cls=torch.tensor([], dtype=torch.float64),
        conf=torch.tensor([], dtype=torch.float64),
    )
    return SimpleNamespace(
        boxes=boxes,
        names={0: "person", 2: "car"},
    )


def test_adapter_converts_fake_yolo_result_to_raw_results() -> None:
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


def test_adapter_returns_empty_list_when_yolo_finds_no_detections() -> None:
    empty_result = make_empty_yolo_result()
    actual_raw_results = build_raw_detections_from_yolo_result(empty_result)
    assert actual_raw_results == []
