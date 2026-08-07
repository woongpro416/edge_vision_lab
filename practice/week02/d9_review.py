# ?? ??: Day 09 Review ? mock inference ??? detection response ??? ?????.

"""Day 09 review: mock inference → postprocessing → response."""

from pathlib import Path

from week01.d6 import read_image_safe
from week02.d8 import prepare_model_input_simple


def run_mock_inference(model_input):
    """Return fixed mock detections for a valid RGB model input."""

    if model_input is None:
        raise ValueError("입력모델이 존재하지 않습니다.")

    if model_input.ndim != 3:
        raise ValueError("입력 모델이 3차원 배열이 아닙니다.")

    if model_input.shape[2] != 3:
        raise ValueError("이미지가 컬러 이미지가 아닙니다")

    raw_results = [
        {"className": "vehicle", "confidence": 0.87},
        {"className": "person", "confidence": 0.76},
    ]
    return raw_results


def count_detections_by_class(raw_results):
    """Count detections by className."""

    if raw_results is None:
        raise ValueError("결과값이 존재하지 않습니다.")

    if not isinstance(raw_results, list):
        raise ValueError("결과값이 list가 아닙니다.")

    class_counts = {}

    for detection in raw_results:
        class_name = detection["className"]
        if class_name not in class_counts:
            class_counts[class_name] = 0

        class_counts[class_name] += 1
    return class_counts


def build_inference_response(raw_results):
    """Build a service response from raw mock detections."""

    if raw_results is None:
        raise ValueError("결과값이 존재하지 않습니다.")

    if not isinstance(raw_results, list):
        raise ValueError("결과값이 list 형태가 아닙니다.")

    class_counts = count_detections_by_class(raw_results)

    response = {
        "status": "OK",
        "detectionCount": len(raw_results),
        "classCounts": class_counts,
        "results": raw_results,
    }

    return response

def main():

    image_path = Path("week01/inputs/sample.jpg")

    bgr_image = read_image_safe(image_path)

    model_input = prepare_model_input_simple(bgr_image, 640, 480)

    raw_results = run_mock_inference(model_input)

    response = build_inference_response(raw_results)

    print(model_input.shape)
    print(len(raw_results))
    print(response)

    assert response["status"] == "OK"
    assert response["detectionCount"] == len(raw_results)
    assert response["classCounts"] == {"vehicle":1, "person":1}
    assert response["results"] == raw_results


if __name__ == "__main__":
    main()
