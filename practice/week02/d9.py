from pathlib import Path

from week01.d6 import read_image_safe
from week02.d8 import prepare_model_input_simple


def run_mock_inference(model_input):
    if model_input is None:
        raise ValueError("입력한 model이 존재하지 않습니다.")
    if model_input.ndim != 3:
        raise ValueError("model_input이 3차원 배열이 아닙니다.")
    if model_input.shape[2] != 3:
        raise ValueError("channel 수가 3이 아닙니다.")

    raw_results = [
        {"className": "vehicle", "confidence": 0.87},
        {"className": "person", "confidence": 0.76},
    ]
    return raw_results


def build_inference_response(raw_results):
    if raw_results is None:
        raise ValueError("raw_results가 존재하지 않습니다.")
    if not isinstance(raw_results, list):
        raise ValueError("반환값이 list가 아닙니다")

    class_counts = count_detections_by_class(raw_results)
    response = {
        "status": "OK",
        "detectionCount": len(raw_results),
        "classCounts": class_counts,
        "results": raw_results,
    }
    return response


def count_detections_by_class(raw_results):
    if raw_results is None:
        raise ValueError("raw_results가 존재하지 않습니다.")
    if not isinstance(raw_results, list):
        raise ValueError("반환값이 list가 아닙니다.")

    class_counts = {}
    for detection in raw_results:
        class_name = detection["className"]
        if class_name not in class_counts:
            class_counts[class_name] = 0
        class_counts[class_name] += 1

    return class_counts


def main():
    image_path = Path("week01/inputs/sample.jpg")
    bgr_image = read_image_safe(image_path)
    model_input = prepare_model_input_simple(bgr_image, 640, 480)
    raw_results = run_mock_inference(model_input)
    response = build_inference_response(raw_results)
    class_counts = count_detections_by_class(raw_results)

    assert response["classCounts"] == class_counts
    assert class_counts == {"vehicle": 1, "person": 1}
    assert model_input is not None
    assert model_input.shape == (480, 640, 3)
    assert isinstance(raw_results, list)
    assert len(raw_results) == 2
    assert isinstance(raw_results[0], dict)
    assert response["status"] == "OK"
    assert response["detectionCount"] == len(raw_results)
    assert response["results"] == raw_results

    print("class_counts:", class_counts)
    print("model_input type:", type(model_input))
    print("raw_results type:", type(raw_results))
    print("raw_results[0] type:", type(raw_results[0]))
    print("response type:", type(response))
    print("model_input shape:", model_input.shape)
    print("raw_results length:", len(raw_results))
    print("response:", response)


if __name__ == "__main__":
    main()
