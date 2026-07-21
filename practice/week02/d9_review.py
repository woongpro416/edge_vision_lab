"""Day 09 review: mock inference → postprocessing → response."""

from pathlib import Path

from week01.d6 import read_image_safe
from week02.d8 import prepare_model_input_simple


def run_mock_inference(model_input):
    """Return fixed mock detections for a valid RGB model input."""
    # TODO: model_input이 None이면 ValueError를 발생시키세요.
    if model_input is None:
        raise ValueError("입력모델이 존재하지 않습니다.")
    # TODO: model_input이 3차원 배열이 아니면 ValueError를 발생시키세요.
    if model_input.ndim != 3:
        raise ValueError("입력 모델이 3차원 배열이 아닙니다.")
    # TODO: channel 수가 3이 아니면 ValueError를 발생시키세요.
    if model_input.shape[2] != 3:
        raise ValueError("이미지가 컬러 이미지가 아닙니다")
    # TODO: vehicle과 person detection이 든 list[dict]를 반환하세요.
    raw_results = [
        {"className": "vehicle", "confidence": 0.87},
        {"className": "person", "confidence": 0.76},
    ]
    return raw_results


def count_detections_by_class(raw_results):
    """Count detections by className."""
    # TODO: raw_results가 None이면 ValueError를 발생시키세요.
    if raw_results is None:
        raise ValueError("결과값이 존재하지 않습니다.")
    # TODO: raw_results가 list가 아니면 ValueError를 발생시키세요.
    if not isinstance(raw_results, list):
        raise ValueError("결과값이 list가 아닙니다.")
    # TODO: 빈 class_counts dict를 만드세요.
    class_counts = {}
    # TODO: raw_results의 각 detection을 순회하세요.
    for detection in raw_results:
        class_name = detection["className"]
        if class_name not in class_counts:
            class_counts[class_name] = 0

        class_counts[class_name] += 1
    return class_counts


def build_inference_response(raw_results):
    """Build a service response from raw mock detections."""
    # TODO: raw_results가 None이면 ValueError를 발생시키세요.
    if raw_results is None:
        raise ValueError("결과값이 존재하지 않습니다.")
    # TODO: raw_results가 list가 아니면 ValueError를 발생시키세요.
    if not isinstance(raw_results, list):
        raise ValueError("결과값이 list 형태가 아닙니다.")
    # TODO: count_detections_by_class(raw_results) 결과를 class_counts에 저장하세요.
    class_counts = count_detections_by_class(raw_results)
    # TODO: status, detectionCount, classCounts, results key를 가진 dict를 반환하세요.
    response = {
        "status": "OK",
        "detectionCount": len(raw_results),
        "classCounts": class_counts,
        "results": raw_results,
    }

    return response

def main():
    # TODO: Path("week01/inputs/sample.jpg")를 image_path에 저장하세요.
    image_path = Path("week01/inputs/sample.jpg")
    # TODO: read_image_safe(image_path) 결과를 bgr_image에 저장하세요.
    bgr_image = read_image_safe(image_path)
    # TODO: prepare_model_input_simple(bgr_image, 640, 480) 결과를 model_input에 저장하세요.
    model_input = prepare_model_input_simple(bgr_image, 640, 480)
    # TODO: run_mock_inference(model_input) 결과를 raw_results에 저장하세요.
    raw_results = run_mock_inference(model_input)
    # TODO: build_inference_response(raw_results) 결과를 response에 저장하세요.
    response = build_inference_response(raw_results)
    # TODO: model_input shape, raw_results 길이, response를 출력하세요.
    print(model_input.shape)
    print(len(raw_results))
    print(response)
    # TODO: response의 status, detectionCount, classCounts를 assert로 검증하세요.
    assert response["status"] == "OK"
    assert response["detectionCount"] == len(raw_results)
    assert response["classCounts"] == {"vehicle":1, "person":1}
    assert response["results"] == raw_results


if __name__ == "__main__":
    main()
