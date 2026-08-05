from pydantic import BaseModel, Field, ValidationError

from pathlib import Path

from week01.d6 import read_image_safe
from week02.d8 import prepare_model_input_simple
from week02.d9 import run_mock_inference
from week02.d10 import filter_detections_by_confidence
from week02.d11 import build_filtered_inference_response

class InferenceResponse(BaseModel):
    # TODO: status는 str field로 선언
    status: str

    # TODO: rawDetectionCount는 int, 0 이상으로 선언
    rawDetectionCount: int = Field(ge=0)

    # TODO: detectionCount는 int, 0 이상으로 선언
    detectionCount: int = Field(ge=0)

    # TODO: confidenceThreshold는 float, 0.0 이상 1.0 이하로 선언
    confidenceThreshold: float = Field(ge=0.0, le=1.0)

    # TODO: classCounts는 dict[str, int]로 선언
    classCounts: dict[str, int]

    # TODO: results 는 list[dict]로 선언
    results: list[dict]


def main():
    image_path = Path("week01/inputs/sample.jpg")
    bgr_image = read_image_safe(image_path)
    model_input = prepare_model_input_simple(bgr_image, 640, 480)
    raw_results = run_mock_inference(model_input)
    threshold = 0.8
    filtered_results = filter_detections_by_confidence(raw_results, threshold)
    response_data = build_filtered_inference_response(raw_results, filtered_results, threshold)

    response_model = InferenceResponse(**response_data)

    # TODO: response_model의 자료형, rawDetectionCount, detectionCount,
    #       results의 실행 시 자료형을 출력한다
    print(type(response_model))
    print(response_model.rawDetectionCount)
    print(response_model.detectionCount)
    print(type(response_model.results))


    serialized_response = response_model.model_dump()
    assert isinstance(response_model, InferenceResponse)
    assert isinstance(serialized_response, dict)

    assert response_model.rawDetectionCount == 2
    assert response_model.detectionCount == 1
    assert response_model.confidenceThreshold == 0.8
    assert serialized_response["status"] == "OK"
    assert serialized_response["results"] == response_data["results"]

    # TODO: response_data의 복사본을 invalid_response_data에 저장한다
    # TODO: confidenceThreshold 를 1.1로 바꾼다
    invalid_response_data = response_data.copy()
    invalid_response_data["confidenceThreshold"] = 1.1

    try:
        # TODO: invalid_response_data로 InferenceResponse를 생성한다
        InferenceResponse(**invalid_response_data)
    except ValidationError:
        print("confidenceThreshold validation failed")

    return serialized_response


if __name__ == "__main__":
    main()
