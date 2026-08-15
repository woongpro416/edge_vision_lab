# Day 22 복습: YOLO-style fields → Adapter → filtering → DetectionResult
# 핵심: Adapter는 형식 변환만 하고 threshold filtering은 convert_detections()가 담당한다.

from week03.d16 import convert_detections
from week04.d21 import build_raw_detection


def build_raw_detections_from_yolo_fields(
    xyxy_boxes: list[list[float]],
    class_ids: list[float],
    confidences: list[float],
    names: dict[int, str],
) -> list[dict]:
    """YOLO-style fields를 서비스 raw detection 목록으로 변환한다."""
    raw_results: list[dict] = []

    # TODO 1: xyxy_boxes, class_ids, confidences를 같은 index 기준으로 순회한다.
    for xyxy, class_id, confidence in zip(
        xyxy_boxes, class_ids, confidences,
    ):
        bbox = [int(value) for value in xyxy]
        class_id_int = int(class_id)
        class_name = names[class_id_int]
        model_detection = {
            "xyxy": bbox,
            "class_id": class_id_int,
            "confidence": confidence,
            "class_name": class_name,
        }

        raw_detection = build_raw_detection(model_detection)

        raw_results.append(raw_detection)

    return raw_results


def main() -> None:
    xyxy_boxes = [
        [15.8, 25.2, 120.6, 230.4],
        [310.1, 110.7, 420.9, 260.3],
    ]
    class_ids = [0.0, 2.0]
    confidences = [0.93, 0.65]
    names = {
        0: "person",
        2: "car",
    }
    threshold = 0.8

    # TODO 6: Adapter를 호출해 raw_results를 만든다.
    raw_results = build_raw_detections_from_yolo_fields(
        xyxy_boxes, class_ids,confidences, names)

    detections = convert_detections(raw_results, threshold)

    print(raw_results)
    print(len(detections))
    print(detections[0].className)

if __name__ == "__main__":
    main()
