# Day 28 복습: Mock Detection Pipeline을 요구사항 기반으로 다시 구현한다.
from week03.d16 import DetectionResult


def build_adapt_detections(model_results: list[dict]) -> list[dict]:
    adapt_detections = []

    for model_result in model_results:
        raw_result = {
            "bbox": model_result["xyxy"],
            "class_id": model_result["class_id"],
            "className": model_result["class_name"],
            "confidence": model_result["confidence"],
        }

        adapt_detections.append(raw_result)

    return adapt_detections


def build_filtered_detections(detections: list[dict], threshold: float) -> list[dict]:
    filtered_detections = []

    for detection in detections:
        if detection["confidence"] >= threshold:
            filtered_detections.append(detection)

    return filtered_detections


def build_dto_detections(detections: list[dict]) -> list[DetectionResult]:
    final_detections = []

    for detection in detections:
        dto_detection = DetectionResult(**detection)
        final_detections.append(dto_detection)

    return final_detections


def build_pipeline(model_results: list[dict], threshold:float) -> list[DetectionResult]:
    adapted_detections = build_adapt_detections(model_results)
    filtered_detections = build_filtered_detections(adapted_detections, threshold)
    dto_detections = build_dto_detections(filtered_detections)

    return dto_detections



if __name__ == "__main__":
    model_results = [
        {
            "xyxy": [40, 60, 180, 260],
            "class_id": 0,
            "class_name": "person",
            "confidence": 0.94,
        },
        {
            "xyxy": [250, 100, 520, 380],
            "class_id": 1,
            "class_name": "vehicle",
            "confidence": 0.70,
        },
        {
            "xyxy": [610, 180, 760, 330],
            "class_id": 2,
            "class_name": "baggage",
            "confidence": 0.52,
        },
    ]

    threshold = 0.70

    results = build_pipeline(model_results, threshold)

    print("최종 결과 수:", len(results))
    print("최종 첫 항목 type:", type(results[0]))
    print("최종 결과:", results)
