"""Day 10 review: rebuild the filtering contract without looking at d10.py."""
from pathlib import Path

from week01.d6 import read_image_safe
from week02.d8 import prepare_model_input_simple
from week02.d9 import build_inference_response, count_detections_by_class, run_mock_inference


def filter_detections_by_confidence(
    raw_results: list[dict], threshold: float
) -> list[dict]:
    # TODO: None, list 타입, threshold None, threshold 범위를 검증한다.
    if raw_results is None:
        raise ValueError(...)

    if not isinstance(raw_results, list):
        raise ValueError(...)

    if threshold is None:
        raise ValueError(...)

    if threshold < 0 or threshold > 1:
        raise ValueError(...)
    # TODO: 새 filtered_results list를 만든다.
    filtered_results = []
    # TODO: raw_results의 detection dict를 순회한다.
    for detection in raw_results:
        if detection["confidence"] >= threshold:
            filtered_results.append(detection)

    # TODO: confidence >= threshold인 detection dict만 새 list에 추가한다.
    # TODO: filtered_results를 반환한다.
    return filtered_results


def main():
    # Path → BGR image → RGB model_input → raw_results를 연결한다.
    image_path = Path("week01/inputs/sample.jpg")
    bgr_image = read_image_safe(image_path)
    model_input = prepare_model_input_simple(bgr_image, 640, 480)
    raw_results = run_mock_inference(model_input)

    threshold = 0.8
    filtered_results = filter_detections_by_confidence(raw_results, threshold)
    filtered_class_counts = count_detections_by_class(filtered_results)
    response = build_inference_response(filtered_results)

    assert len(filtered_results) == 1
    assert response["detectionCount"] == 1

    return response
