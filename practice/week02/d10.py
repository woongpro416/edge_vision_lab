def filter_detections_by_confidence(
    raw_results: list[dict], threshold: float
) -> list[dict]:
    """Return only detections whose confidence is at least threshold.

    Pipeline role:
    raw_results (mock inference output) -> filtered_results -> class count/response
    """
    # TODO 1: raw_results가 None이면 ValueError를 발생시킨다.
    # 이유: None은 "detection이 0개"가 아니라 유효한 결과 자체가 없다는 오류 상태다.
    if raw_results is None:
        raise ValueError("raw_results가 없습니다.")

    # TODO 2: raw_results가 list가 아니면 ValueError를 발생시킨다.
    # 이유: 이 함수는 detection dict가 들어 있는 list를 순회하는 계약을 가진다.
    if not isinstance(raw_results, list):
        raise ValueError("감지결과가 list[dict]형태가 아닙니다.")
    # TODO 3: threshold가 None이면 ValueError를 발생시킨다.
    # 이유: confidence와 비교할 최소 기준값이 없으면 filtering할 수 없다.
    if threshold is None:
        raise ValueError("threshold가 존재하지 않습니다.")
    # TODO 4: threshold가 0보다 작거나 1보다 크면 ValueError를 발생시킨다.
    # 이유: 오늘의 mock confidence 범위는 0.0 이상 1.0 이하다.
    if threshold < 0 or threshold > 1:
        raise ValueError("측정값은 0보다 작거나 1보다 클 수가 없습니다.")
    # 다음 단계: 입력 검증을 직접 작성하고 확인한 뒤,
    # 빈 list 생성 → 순회 → 조건 확인 → append → 반환을 이어서 구현한다.
    filtered_results = []
    
    for detection in raw_results:
        if detection["confidence"] >= threshold:
            filtered_results.append(detection)

    return filtered_results


def main():
    # Image pipeline imports belong here so the pure filtering function can be unit-tested alone.
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
