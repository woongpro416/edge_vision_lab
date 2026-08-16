# Day 23 복습: YOLO Results Adapter를 요구사항만 보고 다시 구현한다.
from typing import Any

from week04.d21 import build_raw_detection


def build_raw_detections_from_yolo_result(result: Any) -> list[dict]:
    raw_results: list[dict] = []

    boxes = result.boxes

    for xyxy, class_id, confidence in zip(
        boxes.xyxy,
        boxes.cls,
        boxes.conf,
    ):
        bbox = [int(value) for value in xyxy.tolist()]
        class_id_int = int(class_id.item())
        confidence_float = float(confidence.item())
        class_name = result.names[class_id_int]

        model_detection = {
            "xyxy": bbox,
            "class_id": class_id_int,
            "confidence": confidence_float,
            "class_name": class_name,
        }

        raw_detection = build_raw_detection(model_detection)
        raw_results.append(raw_detection)

    return raw_results

