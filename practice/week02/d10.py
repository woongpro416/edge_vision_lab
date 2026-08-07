# ?? ??: Day 10 ? confidence threshold? mock detections? filtering???.

def filter_detections_by_confidence(
    raw_results: list[dict], threshold: float
) -> list[dict]:
    """Return only detections whose confidence is at least threshold.

    Pipeline role:
    raw_results (mock inference output) -> filtered_results -> class count/response
    """


    if raw_results is None:
        raise ValueError("raw_results가 없습니다.")



    if not isinstance(raw_results, list):
        raise ValueError("감지결과가 list[dict]형태가 아닙니다.")


    if threshold is None:
        raise ValueError("threshold가 존재하지 않습니다.")


    if threshold < 0 or threshold > 1:
        raise ValueError("측정값은 0보다 작거나 1보다 클 수가 없습니다.")


    filtered_results = []

    for detection in raw_results:
        if detection["confidence"] >= threshold:
            filtered_results.append(detection)

    return filtered_results


def main():

    from pathlib import Path

    from week01.d6 import read_image_safe
    from week02.d8 import prepare_model_input_simple
    from week02.d9 import (
        build_inference_response,
        count_detections_by_class,
        run_mock_inference,
    )

    image_path = Path("week01/inputs/sample.jpg")
    bgr_image = read_image_safe(image_path)
    model_input = prepare_model_input_simple(bgr_image, 640, 480)
    raw_results = run_mock_inference(model_input)
    filtered_results = filter_detections_by_confidence(raw_results, threshold=0.8)
    filtered_class_counts = count_detections_by_class(filtered_results)
    response = build_inference_response(filtered_results)

    assert len(filtered_results) == 1

    return response
