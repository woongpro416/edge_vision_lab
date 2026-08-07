# ?? ??: Day 10 Review ? confidence filtering ??? ?? validation? ?????.

"""Day 10 review: rebuild the filtering contract without looking at d10.py."""
from pathlib import Path

from week01.d6 import read_image_safe
from week02.d8 import prepare_model_input_simple
from week02.d9 import build_inference_response, count_detections_by_class, run_mock_inference


def filter_detections_by_confidence(
    raw_results: list[dict], threshold: float
) -> list[dict]:

    if raw_results is None:
        raise ValueError(...)

    if not isinstance(raw_results, list):
        raise ValueError(...)

    if threshold is None:
        raise ValueError(...)

    if threshold < 0 or threshold > 1:
        raise ValueError(...)

    filtered_results = []

    for detection in raw_results:
        if detection["confidence"] >= threshold:
            filtered_results.append(detection)



    return filtered_results


def main():

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
