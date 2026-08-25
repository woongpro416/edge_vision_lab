# Day 28: Mock Model Output을 Adapter → Filtering → DetectionResult Pipeline으로 변환한다.
from week03.d16 import DetectionResult


def adapt_model_results(model_results: list[dict]) -> list[dict]:
    raw_results = []

    for model_result in model_results:
        raw_result = {
            "bbox": model_result["xyxy"],
            "class_id": model_result["class_id"],
            "className": model_result["class_name"],
            "confidence": model_result["confidence"],
        }

        raw_results.append(raw_result)

    return raw_results


def build_filtered_results(raw_results: list[dict], threshold: float) -> list[dict]:
    filtered_results = []

    for raw_result in raw_results:
        if raw_result["confidence"] >= threshold:
            filtered_results.append(raw_result)

    return filtered_results


def build_final_results(filtered_raw_results: list[dict]) -> list[DetectionResult]:
    final_results = []

    for raw_result in filtered_raw_results:
        detection = DetectionResult(**raw_result)
        final_results.append(detection)

    return final_results


def build_dto_detections(model_results: list[dict], threshold: float) -> list[DetectionResult]:
    adapt_detections = adapt_model_results(model_results)
    filtered_detections = build_filtered_results(adapt_detections, threshold)
    dto_detections = build_final_results(filtered_detections)
    return dto_detections


if __name__ == "__main__":
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

    final_results = build_dto_detections(model_results, threshold)

    print("최종 결과 수:", len(final_results))
    print("최종 첫 항목 type:", type(final_results[0]))
    print("최종 결과:", final_results)
