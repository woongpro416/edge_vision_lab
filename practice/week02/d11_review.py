# 학습 요약: Day 11 복습 — filtering 결과와 response contract 생성을 점검한다.

from pathlib import Path

from week01.d6 import read_image_safe
from week02.d8 import prepare_model_input_simple
from week02.d9 import count_detections_by_class, run_mock_inference
from week02.d10 import filter_detections_by_confidence


def build_filtered_inference_response(
    raw_results: list[dict],
    filtered_results: list[dict],
    threshold: float,
) -> dict:
    if raw_results is None:
        raise ValueError("raw_results must not be None.")
    if not isinstance(raw_results, list):
        raise ValueError("raw_results must be a list.")

    if filtered_results is None:
        raise ValueError("filtered_results must not be None.")
    if not isinstance(filtered_results, list):
        raise ValueError("filtered_results must be a list.")

    if threshold is None:
        raise ValueError("threshold must not be None.")
    if threshold < 0 or threshold > 1:
        raise ValueError("threshold must be between 0 and 1.")

    if len(filtered_results) > len(raw_results):
        raise ValueError("filtered_results must not be longer than raw_results.")

    class_counts = count_detections_by_class(filtered_results)
    response = {
        "status": "OK",
        "rawDetectionCount": len(raw_results),
        "detectionCount": len(filtered_results),
        "confidenceThreshold": threshold,
        "classCounts": class_counts,
        "results": filtered_results,
    }

    return response


def main():
    image_path = Path("week01/inputs/sample.jpg")
    bgr_image = read_image_safe(image_path)
    model_input = prepare_model_input_simple(bgr_image, 640, 480)
    raw_results = run_mock_inference(model_input)

    threshold = 0.8
    filtered_results = filter_detections_by_confidence(raw_results, threshold)
    response = build_filtered_inference_response(
        raw_results, filtered_results, threshold)

    assert response["status"] == "OK"
    assert response["detectionCount"] == 1

    return response


if __name__ == "__main__":
    print(main())
