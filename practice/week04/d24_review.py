# Day 24 재구현: YOLO Result 한 개를 서비스 raw_results로 변환한다.

from typing import Any

from week04.d21 import build_raw_detection


def build_raw_detections_from_yolo_result(result: Any) -> list[dict]:
    """YOLO Result 한 개를 서비스 raw_results로 변환한다."""

    raw_results: list[dict] = []
    boxes = result.boxes

    for xyxy, class_id, confidence in zip(boxes.xyxy, boxes.cls, boxes.conf):
        bbox = [int(value) for value in xyxy.tolist()]
        class_id_int = int(class_id.item())
        confidence_float = float(confidence.item())
        class_name = result.names[class_id_int]

        model_detection = {
            "xyxy": bbox,
            "class_id": class_id_int,
            "class_name": class_name,
            "confidence": confidence_float,
        }

        raw_detection = build_raw_detection(model_detection)
        raw_results.append(raw_detection)

    return raw_results
