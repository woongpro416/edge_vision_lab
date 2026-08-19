# Day 25 복습: Model Postprocessing 결과 → Adapter → Service Filtering

from week03.d16 import convert_detections
from week04.d21 import build_raw_detection


def build_raw_results_from_model_candidates(model_candidates: list[dict]) -> list[dict]:
    """Model 결과를 서비스 raw_results 계약으로 변환한다."""
    raw_results: list[dict] = []

    for model_detection in model_candidates:
        bbox = [int(value) for value in model_detection['xyxy']]

        raw_detection = build_raw_detection(
            {
                "xyxy": bbox,
                "class_id": model_detection["class_id"],
                "class_name": model_detection["class_name"],
                "confidence": model_detection["confidence"],
            }
        )

        raw_results.append(raw_detection)

    return raw_results


def main() -> list:
    model_candidates = [
        {
            "xyxy": [10.8, 20.2, 100.9, 200.7],
            "class_id": 0,
            "class_name": "person",
            "confidence": 0.91,
        },
        {
            "xyxy": [150.4, 30.8, 300.2, 220.5],
            "class_id": 2,
            "class_name": "car",
            "confidence": 0.72,
        },
        {
            "xyxy": [320.6, 50.1, 400.3, 180.9],
            "class_id": 0,
            "class_name": "person",
            "confidence": 0.55,
        },
    ]
    service_threshold = 0.7

    raw_results = build_raw_results_from_model_candidates(model_candidates)

    detections = convert_detections(raw_results, service_threshold)

    print("model detections | raw_results | service detections")
    print(f"{len(model_candidates)} | {len(raw_results)} | {len(detections)}")

    return detections


if __name__ == "__main__":
    main()
