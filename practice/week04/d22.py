# Day 22 실습: YOLO-style fields를 서비스 raw_results로 변환하는 Adapter
# 흐름: YOLO fields → Adapter → application raw_results

from week04.d21 import build_raw_detection


def build_raw_detections_from_yolo_fields(
        xyxy_boxes: list[list[float]],
        class_ids: list[float],
        confidences: list[float],
        names: dict[int, str],
) -> list[dict]:
    raw_results: list[dict] = []

    for xyxy, class_id, confidence in zip(
        xyxy_boxes, class_ids, confidences,
    ):
        bbox = [int(value) for value in xyxy]
        class_id_int = int(class_id)
        class_name = names[class_id_int]
        model_detection = {
            "xyxy": bbox,
            "class_id": class_id_int,
            "class_name": class_name,
            "confidence": confidence,
        }

        raw_detection = build_raw_detection(model_detection)

        raw_results.append(raw_detection)

    return raw_results


def main() -> None:
    xyxy_boxes = [
        [10.0, 20.0, 110.0, 220.0],
        [300.0, 100.0, 400.0, 250.0],
    ]
    class_ids = [0.0, 2.0]
    confidences = [0.91, 0.72]
    names = {
        0: "person",
        2: "car",
    }

    raw_results = build_raw_detections_from_yolo_fields(
        xyxy_boxes,
        class_ids,
        confidences,
        names
    )

    print(raw_results)


if __name__ == "__main__":
    main()
